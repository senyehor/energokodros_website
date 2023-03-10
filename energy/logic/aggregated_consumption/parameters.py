import datetime
from dataclasses import dataclass
from datetime import date, datetime, time
from enum import StrEnum
from typing import TypeAlias, TypedDict, Union

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.types import HOUR
from institutions.models import Facility

AnyQueryParameters: TypeAlias = 'CommonQueryParameters'


class EnergyConsumptionQueryRawParameters(TypedDict, total=False):
    facility_pk: str
    aggregation_interval_seconds: str
    period_start_epoch_seconds: str
    period_end_epoch_seconds: str
    # one hour interval specific filters
    hours_filtering_start_hour: str
    hours_filtering_end_hour: str
    hour_filtering_method: str


@dataclass(kw_only=True)
class CommonQueryParameters:
    facility_to_get_consumption_for_or_all_descendants_if_any: Facility
    aggregation_interval: AggregationIntervalSeconds
    period_start: date
    period_end: date

    @property
    def period_end(self) -> datetime:
        return datetime.combine(
            self._period_end,
            self.__create_one_second_to_midnight_time()
        )

    @period_end.setter
    def period_end(self, value: datetime):
        # noinspection PyAttributeOutsideInit
        self._period_end = value

    @property
    def period_start(self) -> datetime:
        return datetime.combine(
            self._period_start,
            self.__create_all_zeros_time()
        )

    @period_start.setter
    def period_start(self, value: date):
        # noinspection PyAttributeOutsideInit
        self._period_start = value

    def __create_one_second_to_midnight_time(self) -> time:
        return time(23, 59, 59)

    def __create_all_zeros_time(self) -> time:
        return time(0, 0, 0)


@dataclass(kw_only=True)
class OneHourAggregationIntervalQueryParameters(CommonQueryParameters):
    aggregation_interval = AggregationIntervalSeconds.ONE_HOUR
    hours_filtering_method: Union['HourFilteringMethods', None]
    hours_filtering_start_hour: HOUR | None
    hours_filtering_end_hour: HOUR | None

    class HourFilteringMethods(StrEnum):
        EVERY_DAY = 'filter-every-day'
        WHOLE_INTERVAL = 'filter-whole-interval'

    @property
    def filter_every_day(self) -> bool:
        return self.hours_filtering_start_hour is not None \
            and self.hours_filtering_end_hour is not None \
            and self.__hour_filtering_method_every_day

    @property
    def period_start(self) -> datetime:
        if self.__hour_filtering_method_every_day:
            return super().period_start
        if self.__hour_filtering_method_whole_interval:
            return datetime.combine(
                self._period_start,
                time(self.hours_filtering_start_hour, 00, 00)
            )

    @property
    def period_end(self) -> datetime:
        if self.__hour_filtering_method_every_day:
            return super().period_start
        if self.__hour_filtering_method_whole_interval:
            return datetime.combine(
                self._period_end,
                time(self.hours_filtering_end_hour, 00, 00)
            )

    @property
    def __hour_filtering_method_every_day(self) -> bool:
        return self.hours_filtering_method == self.HourFilteringMethods.EVERY_DAY

    @property
    def __hour_filtering_method_whole_interval(self) -> bool:
        return self.hours_filtering_method == self.HourFilteringMethods.WHOLE_INTERVAL
