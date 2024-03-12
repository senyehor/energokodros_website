from abc import ABC
from datetime import date, timedelta
from enum import IntEnum
from typing import Iterable, Type, TypeAlias, TypedDict

from django.db import connection

from energy.logic.aggregated_consumption.exceptions import FacilityAndDescendantsHaveNoSensors
from energy.logic.aggregated_consumption.formatters import (
    OneHourFormatter,
    OneMonthFormatter, RawAggregatedDataFormatter,
)
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters, CommonQueryParameters, OneHourAggregationIntervalQueryParameters,
)
from energy.logic.aggregated_consumption.types import (
    AggregatedConsumptionData, AggregatedConsumptionDataWithTotalConsumption,
    FormattedTotalConsumption, RawAggregatedConsumptionData,
    RawAggregatedConsumptionDataWithRawTotalConsumption, RawConsumptionTime,
    RawConsumptionValue, RawTotalConsumption,
)
from energy.models import BoxSensorSet

AnyQuerier: TypeAlias = '_AggregatedConsumptionQuerierBase'


class AggregatedConsumptionQuerier:
    def __init__(self, parameters: AnyQueryParameters):
        self.__parameters = parameters

    def get_formatted_consumption_with_formatted_total_consumption(self) \
            -> AggregatedConsumptionDataWithTotalConsumption | None:
        querier = self.__get_querier_for_parameters()
        return querier(self.__parameters).get_formatted_consumption_with_total_consumption()

    def get_raw_consumption_with_raw_total_consumption(self) -> \
            RawAggregatedConsumptionDataWithRawTotalConsumption | None:
        querier = self.__get_querier_for_parameters()
        return querier(self.__parameters).get_raw_consumption_with_total_consumption()

    def __get_querier_for_parameters(self) -> Type[AnyQuerier]:
        return _AGGREGATION_INTERVAL_TO_QUERIER_MAPPING[self.__parameters.aggregation_interval]

    @property
    def formatter(self) -> RawAggregatedDataFormatter:
        return self.__get_querier_for_parameters().formatter


class _AggregatedConsumptionQuerierBase(ABC):
    SELECT_PART: str = None
    GROUP_BY_PART: str = None
    ORDER_BY_PART: str = None

    __CONSUMPTION_CTE_START = 'WITH consumption AS ('
    __CONSUMPTION_EXPRESSION = 'TRUNC(SUM(sensor_value), 7)'
    __CONSUMPTION_QUERY_SELECT_WITH_FROM = 'SELECT {select}, ' + f"""
            {__CONSUMPTION_EXPRESSION} AS consumption
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
        ORDER BY {order_by}
    """
    __CONSUMPTION_CTE_END = '),'
    __TOTAL_CONSUMPTION_CTE = """
        total_consumption AS (SELECT SUM(consumption) as total_consumption FROM consumption)
    """
    __MAIN_SELECT = "SELECT * FROM consumption, total_consumption;"
    formatter: RawAggregatedDataFormatter = RawAggregatedDataFormatter()

    class __RawAggregatedConsumptionDataIndexes(IntEnum):
        TIME_PART = 0
        CONSUMPTION_PART = 1

    class __ConsumptionWithTotalConsumptionRawsIndexes(IntEnum):
        TIME_PART = 0
        CONSUMPTION_PART = 1
        TOTAL_CONSUMPTION_PART = 2

    class __BoxesSetIdSubqueryParameters(TypedDict):
        boxes_set_id_subquery: str
        id_or_ids_to_filter: str | int

    def __init__(self, parameters: AnyQueryParameters):
        if self.__class__ == _AggregatedConsumptionQuerierBase:
            raise NotImplementedError('this class must be subclassed')
        self.__parameters = parameters

    def get_formatted_consumption_with_total_consumption(self) \
            -> AggregatedConsumptionDataWithTotalConsumption | None:
        _ = self.get_raw_consumption_with_total_consumption()
        if _:
            raw_consumption, raw_total_consumption = _
            return (
                self.__format_consumption(raw_consumption),
                self.__format_total_consumption(raw_total_consumption)
            )
        return None

    def get_raw_consumption_with_total_consumption(self) \
            -> RawAggregatedConsumptionDataWithRawTotalConsumption | None:
        with connection.cursor() as cursor:
            cursor.execute(self.__compose_query())
            rows = cursor.fetchall()
        if rows:
            return self.__split_rows_into_raw_consumption_and_total_consumption(rows)
        return None

    def __split_rows_into_raw_consumption_and_total_consumption(
            self, rows: list[RawConsumptionTime, RawConsumptionValue, RawTotalConsumption]
    ) -> RawAggregatedConsumptionDataWithRawTotalConsumption:
        _ = self.__ConsumptionWithTotalConsumptionRawsIndexes
        raw_aggregated_consumption = (
            (
                row[_.TIME_PART],
                row[_.CONSUMPTION_PART]
            )
            for row in rows
        )
        raw_total_consumption = rows[0][_.TOTAL_CONSUMPTION_PART]
        # noinspection PyTypeChecker
        return raw_aggregated_consumption, raw_total_consumption

    def __compose_query(self) -> str:
        return ' '.join(
            (
                self.__CONSUMPTION_CTE_START,
                self.__compose_select(),
                self._compose_where(),
                self.__compose_group_by_and_order_by(),
                self.__CONSUMPTION_CTE_END,
                self.__TOTAL_CONSUMPTION_CTE,
                self.__MAIN_SELECT
            )
        )

    def __compose_select(self) -> str:
        return self.__CONSUMPTION_QUERY_SELECT_WITH_FROM.format(
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
        ids = self.__get_box_set_ids_for_facility()
        ids = (str(_id) for _id in ids)
        return ', '.join(ids)

    def __get_box_set_ids_for_facility(self) -> Iterable[int]:
        facility = self.__parameters.facility_to_get_consumption_for_or_all_descendants_if_any
        facility_and_descendants = facility.get_tree(facility)
        ids = BoxSensorSet.objects. \
            only('pk'). \
            filter(facility__in=facility_and_descendants). \
            values_list('pk', flat=True)
        if ids:
            return ids
        raise FacilityAndDescendantsHaveNoSensors

    def __format_consumption(self, raw_consumption: RawAggregatedConsumptionData) \
            -> AggregatedConsumptionData:
        _ = self.__RawAggregatedConsumptionDataIndexes
        return [
            (
                self.formatter.format_time(line[_.TIME_PART]),
                self.formatter.format_consumption(line[_.CONSUMPTION_PART])
            )
            for line in raw_consumption
        ]

    def __format_total_consumption(self, raw_total_consumption: RawTotalConsumption) \
            -> FormattedTotalConsumption:
        return self.formatter.format_total_consumption(raw_total_consumption)

    @property
    def parameters(self) -> CommonQueryParameters:
        return self.__parameters


class __QueryingForCurrentDayMixin(_AggregatedConsumptionQuerierBase):
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


class _OneHourQuerier(__QueryingForCurrentDayMixin, _AggregatedConsumptionQuerierBase):
    SELECT_PART = 'aggregation_interval_start:: TIMESTAMP WITHOUT TIME ZONE AS time'
    GROUP_BY_PART = 'time'
    ORDER_BY_PART = GROUP_BY_PART

    __ADDITIONAL_HOURS_WHERE_FILTERS_FOR_FILTER_EVERY_DAY = """
        AND EXTRACT(HOUR FROM aggregation_interval_start) >= {hours_filtering_start_hour}
        AND EXTRACT(HOUR FROM aggregation_interval_start) <= {hours_filtering_end_hour}
    """

    formatter = OneHourFormatter()

    def _compose_where(self) -> str:
        base_where = super()._compose_where()
        if self.parameters.filter_every_day:
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
        return self.__ADDITIONAL_HOURS_WHERE_FILTERS_FOR_FILTER_EVERY_DAY.format(
            hours_filtering_start_hour=self.parameters.hours_filtering_start_hour,
            hours_filtering_end_hour=self.parameters.hours_filtering_end_hour
        )

    @property
    def parameters(self) -> OneHourAggregationIntervalQueryParameters:
        # typehint correct parameters type for this querier
        # noinspection PyTypeChecker
        return super().parameters


class _OneDayQuerier(__QueryingForCurrentDayMixin, _AggregatedConsumptionQuerierBase):
    SELECT_PART = 'aggregation_interval_start::date AS date'
    GROUP_BY_PART = 'date'
    ORDER_BY_PART = GROUP_BY_PART


class _OneWeekQuerier(_AggregatedConsumptionQuerierBase):
    SELECT_PART = """
        DATE_TRUNC('week', aggregation_interval_start)::DATE || ' - ' ||
        (DATE_TRUNC('week', aggregation_interval_start) + '6 days')::DATE AS week
    """
    GROUP_BY_PART = "DATE_TRUNC('week', aggregation_interval_start)"
    ORDER_BY_PART = GROUP_BY_PART


class _OneMonthQuerier(_AggregatedConsumptionQuerierBase):
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


class _OneYearQuerier(_AggregatedConsumptionQuerierBase):
    SELECT_PART = 'EXTRACT(YEAR FROM aggregation_interval_start) AS year'
    GROUP_BY_PART = 'year'
    ORDER_BY_PART = GROUP_BY_PART


_AGGREGATION_INTERVAL_TO_QUERIER_MAPPING: dict[AggregationIntervalSeconds, Type[AnyQuerier]] = \
    {
        AggregationIntervalSeconds.ONE_HOUR:  _OneHourQuerier,
        AggregationIntervalSeconds.ONE_DAY:   _OneDayQuerier,
        AggregationIntervalSeconds.ONE_WEEK:  _OneWeekQuerier,
        AggregationIntervalSeconds.ONE_MONTH: _OneMonthQuerier,
        AggregationIntervalSeconds.ONE_YEAR:  _OneYearQuerier
    }
