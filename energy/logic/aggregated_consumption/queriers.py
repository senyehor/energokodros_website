import calendar
from abc import ABC
from datetime import datetime
from decimal import Decimal
from typing import Type, TypeAlias, TypedDict

from django.db import connection
from django.utils.translation import gettext_lazy as _

from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters,
    CommonQueryParameters, OneHourAggregationIntervalQueryParameters,
)

AggregatedConsumptionQueryRows = list[tuple[datetime | str, Decimal]] | None

AnyQuerier: TypeAlias = \
    Type['OneHourQuerier'] | \
    Type['OneDayQuerier'] | \
    Type['OneWeekQuerier'] | \
    Type['OneMonthQuerier'] | \
    Type['OneYearQuerier']


class AggregatedConsumptionQuerierBase(ABC):
    SELECT_PART: str = None
    GROUP_BY_PART: str = None
    ORDER_BY_PART: str = None

    CUSTOM_FORMATTING: bool = False

    __QUERY_SELECT_WITH_FROM = 'SELECT ' + """
        {select}, 
        ROUND(SUM(sensor_value), 2) AS total_consumption
        FROM sensor_values_h
    """
    __QUERY_WHERE = """
        WHERE aggregation_interval_start >= '{aggregation_interval_start}'
        AND aggregation_interval_end <= '{aggregation_interval_end}'
        AND boxes_set_id IN ({boxes_set_id_subquery})
    """
    __QUERY_GROUP_BY_AND_ORDER_BY = """
        GROUP BY {group_by}
        ORDER BY {order_by};
    """

    class __BoxesSetIdSubqueryParameters(TypedDict):
        boxes_set_id_subquery: str
        id_or_ids_to_filter: str | int

    def __init__(self, params: AnyQueryParameters):
        if self.__class__ == AggregatedConsumptionQuerierBase:
            raise NotImplementedError('this class must be subclassed')
        self.__params = params

    def get_consumption(self) -> AggregatedConsumptionQueryRows:
        non_formatted_rows = self.__get_rows()
        if self.CUSTOM_FORMATTING and non_formatted_rows:
            return self.__format_rows(non_formatted_rows)
        return non_formatted_rows

    def __format_rows(
            self, non_formatted_rows: AggregatedConsumptionQueryRows
    ) -> AggregatedConsumptionQueryRows:
        time_related_part_index, data_index = 0, 1
        return [
            (
                self._format_time_related_row_part(row[time_related_part_index]),
                row[data_index]
            )
            for row in non_formatted_rows
        ]

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
        return self.__QUERY_WHERE.format(
            aggregation_interval_start=self.parameters.period_start,
            aggregation_interval_end=self.parameters.period_end,
            boxes_set_id_subquery=self.__get_boxes_set_id_subquery()
        )

    def __compose_group_by_and_order_by(self) -> str:
        return self.__QUERY_GROUP_BY_AND_ORDER_BY.format(
            group_by=self.GROUP_BY_PART,
            order_by=self.ORDER_BY_PART
        )

    def __get_boxes_set_id_subquery(self) -> str:
        facility = self.parameters.facility_to_get_consumption_for_or_all_descendants_if_any
        if facility.get_descendants().exists():
            descendants_ids_queryset = facility.get_descendants().only('id')
            id_or_ids_to_filter = ','.join(
                str(facility.id) for facility in descendants_ids_queryset
            )
        else:
            id_or_ids_to_filter = facility.id
        return f"""
            SELECT boxes_set_id FROM boxes_sets
            WHERE facility_id IN ({id_or_ids_to_filter})
            """

    def __get_rows(self) -> AggregatedConsumptionQueryRows:
        with connection.cursor() as cursor:
            cursor.execute(
                self.__compose_query()
            )
            return cursor.fetchall() or None

    def _format_time_related_row_part(self, to_format: datetime | str) -> str:
        ...

    @property
    def parameters(self) -> CommonQueryParameters:
        return self.__params


class OneHourQuerier(AggregatedConsumptionQuerierBase):
    SELECT_PART = 'aggregation_interval_start:: TIMESTAMP WITHOUT TIME ZONE AS time'
    GROUP_BY_PART = 'time'
    ORDER_BY_PART = GROUP_BY_PART

    CUSTOM_FORMATTING = True

    __ADDITIONAL_HOURS_WHERE_FILTERS = """
        AND EXTRACT(HOUR FROM aggregation_interval_start) >= {hours_filtering_start_hour}
        AND EXTRACT(HOUR FROM aggregation_interval_start) < {hours_filtering_end_hour}
    """

    def _format_time_related_row_part(self, to_format: datetime | str) -> str:
        # to_format contains start hour as we use aggregation_interval_start in select
        end_hour = str(to_format.hour + 1)
        return to_format.strftime(f'%d-%m-%Y %H:%M - {end_hour.zfill(2)}:%M')

    def _compose_where(self) -> str:
        base_where = super()._compose_where()
        if self.parameters.is_hours_filtering_set():
            return ' '.join(
                (
                    base_where,
                    self.__compose_additional_hours_where_filters()
                )
            )
        return base_where

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


class OneDayQuerier(AggregatedConsumptionQuerierBase):
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

    CUSTOM_FORMATTING = True

    def _format_time_related_row_part(self, to_format: datetime | str) -> str:
        year, month = to_format.split('-')
        month = _(calendar.month_name[int(month)])
        return f'{year} {month}'


class OneYearQuerier(AggregatedConsumptionQuerierBase):
    SELECT_PART = 'EXTRACT(YEAR FROM aggregation_interval_start) AS year'
    GROUP_BY_PART = 'year'
    ORDER_BY_PART = GROUP_BY_PART
