from dataclasses import dataclass
from datetime import date
from typing import TypeAlias, TypedDict

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from institutions.models import Facility

AnyQueryParameters: TypeAlias = 'CommonQueryParameters'
HOUR: TypeAlias = int


class EnergyConsumptionQueryRawParameters(TypedDict):
    role: str
    facility: str
    aggregation_interval_seconds: str
    period_start_epoch_seconds: str
    period_end_epoch_seconds: str
    # one hour interval specific filters
    hours_filtering_start_hour: str | None
    hours_filtering_end_hour: str | None


@dataclass(frozen=True, kw_only=True)
class CommonQueryParameters:
    facility_to_get_consumption_for_or_all_descendants_if_any: Facility
    aggregation_interval: AggregationIntervalSeconds
    period_start: date
    period_end: date


@dataclass(frozen=True, kw_only=True)
class OneHourAggregationIntervalQueryParameters(CommonQueryParameters):
    aggregation_interval = AggregationIntervalSeconds.ONE_HOUR
    hours_filtering_start_hour: HOUR | None = None
    hours_filtering_end_hour: HOUR | None = None

    def is_hours_filtering_set(self):
        return bool(self.hours_filtering_start_hour and self.hours_filtering_end_hour)
