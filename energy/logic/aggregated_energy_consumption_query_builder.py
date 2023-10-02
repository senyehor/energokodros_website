from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum

from django.utils.decorators import classonlymethod

from institutions.models import Facility


@dataclass
class EnergyConsumptionQueryParameters:
    period_start: date
    period_end: date
    aggregation_interval: timedelta
    facility_to_get_consumption_for_or_all_descendants_if_any: Facility

    def __post_init__(self):
        self.__validate()

    def __validate(self):
        self.__check_period_has_at_least_one_interval()

    def __check_period_has_at_least_one_interval(self):
        period_length = self.period_end - self.period_start
        if self.aggregation_interval > period_length:
            raise AggregationIntervalDoesNotFitPeriod


class AggregationIntervalInSeconds(Enum):
    ONE_HOUR = timedelta(hours=1).total_seconds()
    ONE_DAY = timedelta(days=1).total_seconds()
    ONE_WEEK = timedelta(weeks=1).total_seconds()
    ONE_MONTH = timedelta(weeks=4).total_seconds()
    ONE_YEAR = timedelta(weeks=4 * 12).total_seconds()


@dataclass
class EnergyConsumptionQueryParts:
    select_part: str
    group_by_and_order_by_part: str


class EnergyConsumptionQueryBuilder:
    __interval_query_parts_mapping = {
        AggregationIntervalInSeconds.ONE_HOUR:  EnergyConsumptionQueryParts(
            'aggregation_interval_end:: TIMESTAMP WITHOUT TIME ZONE AS time',
            'time'
        ),
        AggregationIntervalInSeconds.ONE_DAY:   EnergyConsumptionQueryParts(
            'aggregation_interval_end::date AS date',
            'date'
        ),
        AggregationIntervalInSeconds.ONE_WEEK:  EnergyConsumptionQueryParts(
            """
            DATE_TRUNC('week', aggregation_interval_end)::DATE || ' - ' ||
            (DATE_TRUNC('week', aggregation_interval_end) + '6 days')::DATE AS week
            """,
            """
            DATE_TRUNC('week', aggregation_interval_end)
            """
        ),
        AggregationIntervalInSeconds.ONE_MONTH: EnergyConsumptionQueryParts(
            """
            EXTRACT(YEAR FROM aggregation_interval_end) || '-' ||
            EXTRACT(MONTH FROM aggregation_interval_end) AS month
            """,
            """
            EXTRACT(YEAR FROM aggregation_interval_end),
            EXTRACT(MONTH FROM aggregation_interval_end)
            """
        ),
        AggregationIntervalInSeconds.ONE_YEAR:  EnergyConsumptionQueryParts(
            'EXTRACT(YEAR FROM aggregation_interval_end) AS year',
            'year'
        )

    }

    # period_start and period_end are not highlighted as values
    # that can be formatted, but everything works alright
    __query_base = """
        SELECT {select_part}, 
        ROUND(SUM(sensor_value), 2) AS total_consumption
        FROM sensor_values_h
        WHERE aggregation_interval_start >= '{period_start}'
          AND aggregation_interval_end <= '{period_end}'
          AND boxes_set_id IN ({boxes_set_ids})
        GROUP BY {group_by_part}
        ORDER BY {order_by_part};
        """
    __query_params: EnergyConsumptionQueryParameters = None

    @classonlymethod
    def build_query(cls, query_params: EnergyConsumptionQueryParameters):
        cls.__query_params = query_params
        query_parts_by_interval: EnergyConsumptionQueryParts = cls.__get_parts_from_query_params()
        return cls.__query_base.format(
            select_part=query_parts_by_interval.select_part,
            period_start=query_params.period_start,
            period_end=query_params.period_end,
            boxes_set_ids=cls.__get_boxes_set_ids_coma_separated(),
            group_by_part=query_parts_by_interval.group_by_and_order_by_part,
            order_by_part=query_parts_by_interval.group_by_and_order_by_part
        )

    @classonlymethod
    def __get_boxes_set_ids_coma_separated(cls) -> str:
        facility = cls.__query_params.facility_to_get_consumption_for_or_all_descendants_if_any
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

    @classonlymethod
    def __get_interval_from_query_params(cls) -> AggregationIntervalInSeconds:
        try:
            return AggregationIntervalInSeconds(
                cls.__query_params.aggregation_interval.total_seconds()
            )
        except ValueError as e:
            raise AggregationIntervalDoesNotExist from e

    @classonlymethod
    def __get_parts_from_query_params(cls) -> EnergyConsumptionQueryParts:
        return cls.__interval_query_parts_mapping[cls.__get_interval_from_query_params()]


class AggregationIntervalDoesNotExist(Exception):
    pass


class AggregationIntervalDoesNotFitPeriod(Exception):
    pass
