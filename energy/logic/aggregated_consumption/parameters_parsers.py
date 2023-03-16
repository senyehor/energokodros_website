import time
from dataclasses import fields
from datetime import date, datetime
from typing import Any, Callable, Iterable, Type, TypeAlias

from energy.logic.aggregated_consumption.exceptions import (
    AggregationIntervalDoesNotFitPeriod, FutureFilteringDate, InvalidHourFilteringMethod,
    PeriodStartGreaterThanEnd,
    QueryParametersInvalid, StartHourGreaterThanEndHour,
)
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters, CommonQueryParameters,
    EnergyConsumptionQueryRawParameters, OneHourAggregationIntervalQueryParameters,
)
from energy.logic.aggregated_consumption.simple import \
    parse_str_parameter_to_int_with_correct_exception
from institutions.models import Facility
from utils.common import get_object_by_hashed_id_or_404

AnyQueryParametersParser: TypeAlias = '_CommonQueryParametersParser'


class ParameterParser:
    def __init__(self, raw_parameters: dict[str, str]):
        self.__raw_parameters = EnergyConsumptionQueryRawParameters(**raw_parameters)

    def get_parameters(self) -> AnyQueryParameters:
        aggregation_interval = self.__extract_aggregation_interval()
        parser = self.__get_parser_for_aggregation_interval(aggregation_interval)
        _ = self.__raw_parameters
        return parser(
            aggregation_interval=aggregation_interval,
            facility_pk_to_get_consumption_for_or_all_descendants_if_any=_.pop('facility_pk'),
            period_end_epoch_seconds=_.pop('period_end_epoch_seconds'),
            period_start_epoch_seconds=_.pop('period_start_epoch_seconds'),
            **_
        ).get_parameters()

    def __extract_aggregation_interval(self) -> AggregationIntervalSeconds:
        aggregation_interval_seconds = parse_str_parameter_to_int_with_correct_exception(
            self.__raw_parameters.pop('aggregation_interval_seconds')
        )
        return AggregationIntervalSeconds(aggregation_interval_seconds)

    def __get_parser_for_aggregation_interval(
            self, aggregation_interval: AggregationIntervalSeconds) \
            -> Type[AnyQueryParametersParser] | Callable:
        return _AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_MAPPING[aggregation_interval]


class _CommonQueryParametersParser:
    def __init__(
            self, *,
            aggregation_interval: AggregationIntervalSeconds,
            facility_pk_to_get_consumption_for_or_all_descendants_if_any: str,
            period_start_epoch_seconds: str,
            period_end_epoch_seconds: str, **kwargs
    ):
        self.__facility_to_get_consumption_for_or_all_descendants_if_any = \
            self.__parse_facility(facility_pk_to_get_consumption_for_or_all_descendants_if_any)
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
        _ = parse_str_parameter_to_int_with_correct_exception
        period_start_epoch_seconds = _(period_start_epoch_seconds)
        period_end_epoch_seconds = _(period_end_epoch_seconds)
        self._period_start = self.__convert_epoch_seconds_to_date(period_start_epoch_seconds)
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

    def __parse_facility(self, facility_pk: str) -> Facility:
        # noinspection PyTypeChecker
        return get_object_by_hashed_id_or_404(Facility, facility_pk)


class __AllowQueryingForCurrentDayParser(_CommonQueryParametersParser):
    def _check_period_contains_at_least_one_aggregation_interval(
            self: _CommonQueryParametersParser):
        if self._period_start == self._period_end:
            return
        super()._check_period_contains_at_least_one_aggregation_interval()


class _OneHourAggregationIntervalQueryParametersParser(__AllowQueryingForCurrentDayParser):
    """one hour aggregation interval has additional parameters"""
    __HOURS: Iterable[int] = range(24)

    def __init__(
            self, *, hours_filtering_start_hour: str = None,
            hours_filtering_end_hour: str = None, hour_filtering_method: str = None,
            **kwargs
    ):
        self.__check_aggregation_interval_is_on_hour(kwargs.get('aggregation_interval'))
        self.__hours_filtering_start_hour = hours_filtering_start_hour
        self.__hours_filtering_end_hour = hours_filtering_end_hour
        self.__hour_filtering_method = hour_filtering_method
        if self.__check_hour_filtering_options_are_set():
            self.__set_hours_filtering_range(hours_filtering_start_hour, hours_filtering_end_hour)
        super().__init__(**kwargs)
        self._validate()

    def get_parameters(self) -> OneHourAggregationIntervalQueryParameters:
        _ = super().get_parameters()
        base_kwargs = {field.name: getattr(_, field.name) for field in fields(_.__class__)}
        return OneHourAggregationIntervalQueryParameters(
            **base_kwargs,
            hours_filtering_start_hour=self.__hours_filtering_start_hour,
            hours_filtering_end_hour=self.__hours_filtering_end_hour,
            hours_filtering_method=self.__hour_filtering_method
        )

    def _validate(self):
        super()._validate()
        if self.__check_hour_filtering_options_are_set():
            self.__check_hours_filtering_range_is_correct()

    def __check_aggregation_interval_is_on_hour(self, aggregation_interval: Any):
        if aggregation_interval is not AggregationIntervalSeconds.ONE_HOUR:
            raise ValueError('this class should work only with one hour aggregation interval')

    def __check_hours_filtering_range_is_correct(self):
        if self.__hours_filtering_start_hour not in self.__HOURS:
            raise QueryParametersInvalid
        if self.__hours_filtering_end_hour not in self.__HOURS:
            raise QueryParametersInvalid
        if self.__hour_filtering_method == \
                OneHourAggregationIntervalQueryParameters.HourFilteringMethods.EVERY_DAY:
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

    def __set_hour_filtering_method(self):
        try:
            self.__hour_filtering_method = \
                OneHourAggregationIntervalQueryParameters.HourFilteringMethods(
                    self.__hour_filtering_method
                )
        except ValueError as e:
            raise InvalidHourFilteringMethod from e

    def __check_hour_filtering_options_are_set(self):
        return self.__hours_filtering_start_hour is not None \
            and self.__hours_filtering_end_hour is not None \
            and self.__hour_filtering_method is not None


class _OneDayAggregationIntervalQueryParametersParser(__AllowQueryingForCurrentDayParser):
    pass


_AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_MAPPING: \
    dict[
        AggregationIntervalSeconds,
        Type[AnyQueryParametersParser]] = \
    {
        AggregationIntervalSeconds.ONE_HOUR:  _OneHourAggregationIntervalQueryParametersParser,
        AggregationIntervalSeconds.ONE_DAY:   _OneDayAggregationIntervalQueryParametersParser,
        AggregationIntervalSeconds.ONE_WEEK:  _CommonQueryParametersParser,
        AggregationIntervalSeconds.ONE_MONTH: _CommonQueryParametersParser,
        AggregationIntervalSeconds.ONE_YEAR:  _CommonQueryParametersParser
    }
