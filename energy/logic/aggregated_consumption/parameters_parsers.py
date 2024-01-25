import time
from dataclasses import fields
from datetime import date, datetime
from typing import Any

from typing_extensions import TypeAlias

from energy.logic.aggregated_consumption.exceptions import (
    AggregationIntervalDoesNotFitPeriod, FutureFilteringDate, PeriodStartGreaterThanEnd,
    QueryParametersInvalid, StartHourGreaterThanEndHour,
)
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import (
    CommonQueryParameters,
    OneHourAggregationIntervalQueryParameters,
)
from energy.logic.aggregated_consumption.simple import \
    parse_str_parameter_to_int_with_correct_exception
from institutions.models import Facility

AnyParametersParser: TypeAlias = 'CommonQueryParametersParser'


class CommonQueryParametersParser:
    def __init__(
            self, *,
            facility_to_get_consumption_for_or_all_descendants_if_any: Facility,
            aggregation_interval: AggregationIntervalSeconds,
            period_start_epoch_seconds: str,
            period_end_epoch_seconds: str
    ):
        self.__facility_to_get_consumption_for_or_all_descendants_if_any = \
            facility_to_get_consumption_for_or_all_descendants_if_any
        self.__aggregation_interval = aggregation_interval
        self.__set_period_boundaries(period_start_epoch_seconds, period_end_epoch_seconds)
        self._validate()

    def get_parameters(self) -> CommonQueryParameters:
        return CommonQueryParameters(
            facility_to_get_consumption_for_or_all_descendants_if_any=
            self.__facility_to_get_consumption_for_or_all_descendants_if_any,
            aggregation_interval=self.__aggregation_interval,
            period_start=self._period_start,
            period_end=self._period_end
        )

    def _validate(self):
        self.__check_period_is_valid()
        self._check_period_contains_at_least_one_aggregation_interval()

    def __set_period_boundaries(self, period_start_epoch_seconds: str,
                                period_end_epoch_seconds: str):
        period_start_epoch_seconds = parse_str_parameter_to_int_with_correct_exception(
            period_start_epoch_seconds
        )
        period_end_epoch_seconds = parse_str_parameter_to_int_with_correct_exception(
            period_end_epoch_seconds
        )
        self._period_start = self.__convert_epoch_seconds_to_date(
            period_start_epoch_seconds
        )
        self._period_end = self.__convert_epoch_seconds_to_date(period_end_epoch_seconds)

    def __check_period_is_valid(self):
        if self._period_start > self._period_end:
            raise PeriodStartGreaterThanEnd

    def _check_period_contains_at_least_one_aggregation_interval(self):
        period_length_seconds = int((self._period_end - self._period_start).total_seconds())
        if period_length_seconds < self.__aggregation_interval:
            raise AggregationIntervalDoesNotFitPeriod

    def __convert_epoch_seconds_to_date(self, epoch_seconds: int) -> date:
        if epoch_seconds < 0:
            raise QueryParametersInvalid
        if int(time.time()) < epoch_seconds:
            # future timestamp (senseless filtering for future dates)
            raise FutureFilteringDate
        return datetime.fromtimestamp(epoch_seconds).date()


class __AllowQueryingForCurrentDayParser(CommonQueryParametersParser):
    def _check_period_contains_at_least_one_aggregation_interval(
            self: CommonQueryParametersParser):
        if self._period_start == self._period_end:
            return
        super()._check_period_contains_at_least_one_aggregation_interval()


class OneHourAggregationIntervalQueryParametersParser(__AllowQueryingForCurrentDayParser):
    """one hour aggregation interval has additional parameters"""
    __HOURS = range(24)

    def __init__(
            self, *, hours_filtering_start_hour: str = None, hours_filtering_end_hour: str = None,
            **kwargs
    ):
        self.__check_aggregation_interval_is_on_hour(kwargs.get('aggregation_interval'))
        self.__hours_filtering_start_hour = hours_filtering_start_hour
        self.__hours_filtering_end_hour = hours_filtering_end_hour
        if hours_filtering_start_hour and hours_filtering_end_hour:
            self.__set_hours_filtering_range(hours_filtering_start_hour, hours_filtering_end_hour)
        super().__init__(**kwargs)
        self._validate()

    def get_parameters(self) -> OneHourAggregationIntervalQueryParameters:
        _ = super().get_parameters()
        base_kwargs = {field.name: getattr(_, field.name) for field in fields(_.__class__)}
        return OneHourAggregationIntervalQueryParameters(
            **base_kwargs,
            hours_filtering_start_hour=self.__hours_filtering_start_hour,
            hours_filtering_end_hour=self.__hours_filtering_end_hour
        )

    def _validate(self):
        super()._validate()
        if self.__check_hours_filtering_set():
            self.__check_hours_filtering_range_is_correct()

    def __check_aggregation_interval_is_on_hour(self, aggregation_interval: Any):
        if aggregation_interval is not AggregationIntervalSeconds.ONE_HOUR:
            raise ValueError('this class should work only with one hour aggregation interval')

    def __check_hours_filtering_range_is_correct(self):
        if self.__hours_filtering_start_hour not in self.__HOURS:
            raise QueryParametersInvalid
        if self.__hours_filtering_end_hour not in self.__HOURS:
            raise QueryParametersInvalid
        if self.__hours_filtering_start_hour > self.__hours_filtering_end_hour:
            raise StartHourGreaterThanEndHour

    def __set_hours_filtering_range(self, hours_filtering_start_hour: str,
                                    hours_filtering_end_hour: str):
        self.__hours_filtering_start_hour = parse_str_parameter_to_int_with_correct_exception(
            hours_filtering_start_hour
        )
        self.__hours_filtering_end_hour = parse_str_parameter_to_int_with_correct_exception(
            hours_filtering_end_hour
        )

    def __check_hours_filtering_set(self):
        return self.__hours_filtering_start_hour and self.__hours_filtering_end_hour


class OneDayAggregationIntervalQueryParametersParser(__AllowQueryingForCurrentDayParser):
    pass
