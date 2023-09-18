from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import TypeAlias, TypedDict, Union

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.types import HOUR
from institutions.models import Facility

AnyQueryParameters: TypeAlias = 'CommonQueryParameters'


class EnergyConsumptionQueryRawParameters(TypedDict, total=False):
    facility_pk: str
    aggregation_interval_seconds: str
    period_start_epoch_seconds_utc: str
    period_end_epoch_seconds_utc: str
    include_forecast: str
    # one hour interval specific filters
    hour_filtering_start_hour: str
    hour_filtering_end_hour: str
    hour_filtering_method: str


@dataclass(kw_only=True)
class CommonQueryParameters:
    facility_to_get_consumption_for_or_all_descendants_if_any: Facility
    aggregation_interval: AggregationIntervalSeconds
    period_start: date
    period_end: date
    include_forecast: bool

    @property
    def period_start(self) -> date:
        return self._period_start

    @period_start.setter
    def period_start(self, value: date):
        # noinspection PyAttributeOutsideInit
        self._period_start = value

    @property
    def period_end(self) -> date:
        return self._period_end

    @period_end.setter
    def period_end(self, value: date):
        # noinspection PyAttributeOutsideInit
        self._period_end = value


@dataclass(kw_only=True)
class OneHourAggregationIntervalQueryParameters(CommonQueryParameters):
    aggregation_interval = AggregationIntervalSeconds.ONE_HOUR
    hour_filtering_method: Union['HourFilteringMethods', None]
    hour_filtering_start_hour: HOUR | None
    hour_filtering_end_hour: HOUR | None

    class HourFilteringMethods(str, Enum):
        EVERY_DAY = 'filter-every-day'
        WHOLE_INTERVAL = 'filter-whole-interval'

    @property
    def filter_every_day(self) -> bool:
        return self.__check_hour_filters_set() and self.__hour_filtering_method_every_day

    @property
    def __hour_filtering_method_every_day(self) -> bool:
        return self.hour_filtering_method == self.HourFilteringMethods.EVERY_DAY

    def __hour_filtering_method_whole_interval(self) -> bool:
        return self.hour_filtering_method == self.HourFilteringMethods.WHOLE_INTERVAL

    def __check_hour_filters_set(self) -> bool:
        return self.hour_filtering_start_hour is not None \
            and self.hour_filtering_end_hour is not None
