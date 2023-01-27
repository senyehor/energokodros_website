from abc import ABC
from datetime import date, timedelta
from enum import IntEnum
from typing import TypeAlias, TypedDict

from django.db import connection

from energy.logic.aggregated_consumption.exceptions import NoConsumptionData
from energy.logic.aggregated_consumption.formatters import (
    AnyFormatter, CommonFormatter, OneHourFormatter,
    OneMonthFormatter,
)
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters, CommonQueryParameters, OneHourAggregationIntervalQueryParameters,
)
from energy.logic.aggregated_consumption.simple import get_box_set_ids_for_facility
from energy.logic.aggregated_consumption.types import (
    RawAggregatedConsumptionData,
)


class AggregatedConsumptionQuerierBase(ABC):
    SELECT_PART: str = None
    GROUP_BY_PART: str = None
    ORDER_BY_PART: str = None

    __TOTAL_CONSUMPTION_EXPRESSION = 'TRUNC(SUM(sensor_value), 7)'
    __QUERY_SELECT_WITH_FROM = 'SELECT {select}, ' + f"""
        {__TOTAL_CONSUMPTION_EXPRESSION} AS total_consumption
        FROM sensor_values_h
    """
    __QUERY_WHERE_INTERVAL = """
        WHERE aggregation_interval_start >= '{aggregation_interval_start}'
        AND aggregation_interval_end <= '{aggregation_interval_end}'
    """
    __QUERY_WHERE_BOXES_SETS = """
        AND boxes_set_id IN ({box_set_ids})
    """
    __QUERY_GROUP_BY_AND_ORDER_BY = """
        GROUP BY {group_by}
        ORDER BY {order_by};
    """

    formatter: AnyFormatter = CommonFormatter()

    class __RawAggregatedConsumptionDataIndexes(IntEnum):
        TIME_PART = 0
        CONSUMPTION_PART = 1

    class __BoxesSetIdSubqueryParameters(TypedDict):
        boxes_set_id_subquery: str
        id_or_ids_to_filter: str | int

    def __init__(self, parameters: AnyQueryParameters):
        if self.__class__ == AggregatedConsumptionQuerierBase:
            raise NotImplementedError('this class must be subclassed')
        self.__parameters = parameters

    def get_consumption(self) -> RawAggregatedConsumptionData:
        with connection.cursor() as cursor:
            cursor.execute(self.__compose_query())
            consumption = cursor.fetchall()
            if not consumption:
                raise NoConsumptionData
            return consumption

    def __compose_query(self) -> str:
        return ' '.join(
            (
                self.__compose_select(),
                self._compose_where(),
                self.__compose_group_by_and_order_by()
            )
        )

    def __compose_select(self) -> str:
        return self.__QUERY_SELECT_WITH_FROM.format(
            select=self.SELECT_PART
        )

    def _compose_where(self) -> str:
        return ' '.join(
            (
                self._compose_where_interval(),
                self.__compose_where_boxes_sets()
            )
        )

    def _compose_where_interval(self) -> str:
        return self.__QUERY_WHERE_INTERVAL.format(
            aggregation_interval_start=self.parameters.period_start,
            aggregation_interval_end=self.parameters.period_end,
        )

    def __compose_where_boxes_sets(self) -> str:
        return self.__QUERY_WHERE_BOXES_SETS.format(
            box_set_ids=self.__get_boxes_set_ids()
        )

    def __compose_group_by_and_order_by(self) -> str:
        return self.__QUERY_GROUP_BY_AND_ORDER_BY.format(
            group_by=self.GROUP_BY_PART,
            order_by=self.ORDER_BY_PART
        )

    def __get_boxes_set_ids(self) -> str:
        ids = get_box_set_ids_for_facility(
            self.parameters.facility_to_get_consumption_for_or_all_descendants_if_any
        )
        ids = (str(_id) for _id in ids)
        return ', '.join(ids)

    @property
    def parameters(self) -> CommonQueryParameters:
        return self.__parameters


class __QueryingForCurrentDayMixin(AggregatedConsumptionQuerierBase):
    __CURRENT_DAY_WHERE = """
    WHERE
        aggregation_interval_start >= '{current_date}'
    AND aggregation_interval_start <= '{next_day_date}'
    """
    __current_date: date = None

    def _compose_where_interval(self) -> str:
        if self.__check_querying_is_for_current_day():
            return self.__compose_current_day_where()
        return super()._compose_where_interval()

    def __compose_current_day_where(self) -> str:
        next_day_date = self.__current_date + timedelta(days=1)
        return self.__CURRENT_DAY_WHERE.format(
            current_date=self.__current_date,
            next_day_date=next_day_date
        )

    def __check_querying_is_for_current_day(self) -> bool:
        if self.parameters.period_start == self.parameters.period_end:
            self.__current_date = self.parameters.period_start
            return True
        return False


class OneHourQuerier(__QueryingForCurrentDayMixin, AggregatedConsumptionQuerierBase):
    SELECT_PART = 'aggregation_interval_start:: TIMESTAMP WITHOUT TIME ZONE AS time'
    GROUP_BY_PART = 'time'
    ORDER_BY_PART = GROUP_BY_PART

    __ADDITIONAL_HOURS_WHERE_FILTERS = """
        AND EXTRACT(HOUR FROM aggregation_interval_start) >= {hours_filtering_start_hour}
        AND EXTRACT(HOUR FROM aggregation_interval_start) <= {hours_filtering_end_hour}
    """
    formatter = OneHourFormatter()

    def _compose_where(self) -> str:
        base_where = super()._compose_where()
        if self.parameters.is_hours_filtering_set():
            return self.__add_hours_filter_to_base_where(base_where)
        return base_where

    def __add_hours_filter_to_base_where(self, base_where: str) -> str:
        return ' '.join(
            (
                base_where,
                self.__compose_additional_hours_where_filters()
            )
        )

    def __compose_additional_hours_where_filters(self) -> str:
        return self.__ADDITIONAL_HOURS_WHERE_FILTERS.format(
            hours_filtering_start_hour=self.parameters.hours_filtering_start_hour,
            hours_filtering_end_hour=self.parameters.hours_filtering_end_hour
        )

    @property
    def parameters(self) -> OneHourAggregationIntervalQueryParameters:
        # typehint correct parameters type for this querier
        # noinspection PyTypeChecker
        return super().parameters


class OneDayQuerier(__QueryingForCurrentDayMixin, AggregatedConsumptionQuerierBase):
    SELECT_PART = 'aggregation_interval_start::date AS date'
    GROUP_BY_PART = 'date'
    ORDER_BY_PART = GROUP_BY_PART


class OneWeekQuerier(AggregatedConsumptionQuerierBase):
    SELECT_PART = """
        DATE_TRUNC('week', aggregation_interval_start)::DATE || ' - ' ||
        (DATE_TRUNC('week', aggregation_interval_start) + '6 days')::DATE AS week
    """
    GROUP_BY_PART = "DATE_TRUNC('week', aggregation_interval_start)"
    ORDER_BY_PART = GROUP_BY_PART


class OneMonthQuerier(AggregatedConsumptionQuerierBase):
    SELECT_PART = """
        EXTRACT(YEAR FROM aggregation_interval_start) || '-' ||
        EXTRACT(MONTH FROM aggregation_interval_start) AS month
    """
    GROUP_BY_PART = """
        EXTRACT(YEAR FROM aggregation_interval_start),
        EXTRACT(MONTH FROM aggregation_interval_start)
    """
    ORDER_BY_PART = GROUP_BY_PART
    formatter = OneMonthFormatter()


class OneYearQuerier(AggregatedConsumptionQuerierBase):
    SELECT_PART = 'EXTRACT(YEAR FROM aggregation_interval_start) AS year'
    GROUP_BY_PART = 'year'
    ORDER_BY_PART = GROUP_BY_PART


AnyQuerier: TypeAlias = 'AggregatedConsumptionQuerierBase'
