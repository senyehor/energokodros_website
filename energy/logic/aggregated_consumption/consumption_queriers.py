from abc import ABC
from datetime import datetime, time, timedelta
from enum import IntEnum
from typing import Iterable, Type, TypeAlias, TypedDict

from django.db import connection

from energy.logic.aggregated_consumption.formatters import (
    CommonFormatter, OneHourFormatter, OneMonthFormatter,
)
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters, CommonQueryParameters, OneHourAggregationIntervalQueryParameters,
)
from energy.logic.aggregated_consumption.types import (
    Consumption, ConsumptionRawAndFormatted, ConsumptionRecord,
    ConsumptionRecordRawAndFormatted, RawConsumption,
    RawConsumptionRecord,
    RawConsumptionWithRawTotalConsumption, RawQueryRows, RawTotalConsumption,
    TotalConsumption,
)
from energy.logic.aggregated_consumption.verbose_exceptions_for_user import \
    FacilityAndDescendantsHaveNoSensors
from energy.models import BoxSensorSet
from institutions.logic import get_all_descendants_of_facility_with_self

AnyQuerier: TypeAlias = '_AggregatedConsumptionQuerierBase'


class AggregatedConsumptionQuerier:
    __raw_consumption: RawConsumption
    __raw_total_consumption: RawTotalConsumption

    def __init__(self, parameters: AnyQueryParameters):
        self.__parameters = parameters
        self.__querier = self.__get_querier_type()(self.__parameters)
        self.__formatter = self.__querier.formatter
        self.__query()

    def get_formatted_consumption(self) -> Consumption | None:
        if self.__raw_consumption:
            return [
                ConsumptionRecord(
                    time=self.__formatter.format_time(row.time),
                    value=self.__formatter.format_consumption(row.value)
                )
                for row in self.__raw_consumption
            ]
        return None

    def get_raw_and_formatted_consumption(self) -> ConsumptionRawAndFormatted | None:
        if self.__raw_consumption:
            return [
                ConsumptionRecordRawAndFormatted(
                    raw_consumption_record=row,
                    formatted_consumption_record=ConsumptionRecord(
                        time=self.__formatter.format_time(row.time),
                        value=self.__formatter.format_consumption(row.value)
                    )
                )
                for row in self.__raw_consumption
            ]
        return None

    def get_formatted_total_consumption(self) -> TotalConsumption | None:
        if self.__raw_total_consumption:
            return self.__formatter.format_total_consumption(self.__raw_total_consumption)
        return None

    def __query(self):
        consumption_with_total_consumption = \
            self.__querier.get_raw_consumption_with_raw_total_consumption()
        self.__raw_consumption, self.__raw_total_consumption = consumption_with_total_consumption

    def __get_querier_type(self) -> Type[AnyQuerier]:
        return _AGGREGATION_INTERVAL_TO_QUERIER_MAPPING[self.__parameters.aggregation_interval]


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

    formatter: CommonFormatter = CommonFormatter()

    class __ConsumptionWithTotalConsumptionRowsIndexes(IntEnum):
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

    def get_raw_consumption_with_raw_total_consumption(self) \
            -> RawConsumptionWithRawTotalConsumption | tuple[None, None]:
        with connection.cursor() as cursor:
            cursor.execute(self.__compose_query())
            rows = cursor.fetchall()
        if rows:
            return self.__split_rows_into_raw_consumption_and_total_consumption(rows)
        return None, None

    def __split_rows_into_raw_consumption_and_total_consumption(
            self, rows: RawQueryRows
    ) -> RawConsumptionWithRawTotalConsumption:
        _ = self.__ConsumptionWithTotalConsumptionRowsIndexes
        raw_aggregated_consumption = (
            RawConsumptionRecord(
                time=row[_.TIME_PART],
                value=row[_.CONSUMPTION_PART]
            )
            for row in rows
        )
        raw_total_consumption = self.__extract_raw_total_consumption(rows)
        return raw_aggregated_consumption, raw_total_consumption

    def __extract_raw_total_consumption(self, rows: RawQueryRows) -> RawTotalConsumption:
        _ = self.__ConsumptionWithTotalConsumptionRowsIndexes
        # take any row, as total consumption is the same in every row
        return rows[0][_.TOTAL_CONSUMPTION_PART]

    def __compose_query(self) -> str:
        return ' '.join(
            (
                self.__CONSUMPTION_CTE_START,
                self.__compose_select(),
                self._compose_where(
                    period_start=self._make_period_start_00_00(),
                    period_end=self._make_period_end_shifted_one_day_forward_00_00()
                ),
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

    def _compose_where(self, period_start: datetime, period_end: datetime) -> str:
        return ' '.join(
            (
                self.__compose_interval_where(period_start=period_start, period_end=period_end),
                self.__compose_boxes_sets_where_()
            )
        )

    def _make_period_start_00_00(self) -> datetime:
        return datetime.combine(
            self.parameters.period_start,
            time(hour=00)
        )

    def _make_period_end_shifted_one_day_forward_00_00(self) -> datetime:
        # in order to filter aggregation interval end correctly, period end must be shifted
        # one day forward, as we want to include 23 - 00 interval, where 00 is already a part
        # of the following day
        return datetime.combine(
            self.parameters.period_end + timedelta(days=1),
            time(hour=00)
        )

    def __compose_interval_where(
            self, period_start: datetime, period_end: datetime
    ) -> str:
        return self.__QUERY_WHERE_INTERVAL.format(
            aggregation_interval_start=period_start,
            aggregation_interval_end=period_end,
        )

    def __compose_boxes_sets_where_(self) -> str:
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
        facility_and_descendants = get_all_descendants_of_facility_with_self(facility)
        ids = BoxSensorSet.objects. \
            only('pk'). \
            filter(facility__in=facility_and_descendants). \
            values_list('pk', flat=True)
        if ids:
            return ids
        raise FacilityAndDescendantsHaveNoSensors

    @property
    def parameters(self) -> CommonQueryParameters:
        return self.__parameters


class _OneHourQuerier(_AggregatedConsumptionQuerierBase):
    SELECT_PART = 'aggregation_interval_start AS time'
    GROUP_BY_PART = 'time'
    ORDER_BY_PART = GROUP_BY_PART

    __ADDITIONAL_HOURS_WHERE_FILTERS_FOR_FILTER_EVERY_DAY = """
        AND EXTRACT(HOUR FROM aggregation_interval_start) >= {hour_filtering_start_hour}
        AND EXTRACT(HOUR FROM aggregation_interval_start) <= {hour_filtering_end_hour}
    """

    formatter = OneHourFormatter()

    def _compose_where(self, period_start: datetime, period_end: datetime) -> str:
        if self.parameters.filter_whole_interval:
            return super()._compose_where(
                period_start=self.__create_period_start_for_filtering_whole_interval(),
                period_end=self.__create_period_end_for_filtering_whole_interval()
            )
        base_where = super()._compose_where(
            period_start=self._make_period_start_00_00(),
            period_end=self._make_period_end_shifted_one_day_forward_00_00()
        )
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

    def __create_period_start_for_filtering_whole_interval(self) -> datetime:
        return datetime.combine(
            self.parameters.period_start,
            time(hour=self.parameters.hour_filtering_start_hour)
        )

    def __create_period_end_for_filtering_whole_interval(self) -> datetime:
        return datetime.combine(
            self.parameters.period_end,
            time(hour=self.parameters.hour_filtering_end_hour)
        )

    def __compose_additional_hours_where_filters(self) -> str:
        return self.__ADDITIONAL_HOURS_WHERE_FILTERS_FOR_FILTER_EVERY_DAY.format(
            hour_filtering_start_hour=self.parameters.hour_filtering_start_hour,
            hour_filtering_end_hour=self.parameters.hour_filtering_end_hour
        )

    @property
    def parameters(self) -> OneHourAggregationIntervalQueryParameters:
        # typehint correct parameters type for this querier
        # noinspection PyTypeChecker
        return super().parameters


class _OneDayQuerier(_AggregatedConsumptionQuerierBase):
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
