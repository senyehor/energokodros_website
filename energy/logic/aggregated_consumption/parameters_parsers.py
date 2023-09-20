import time
from calendar import monthrange
from dataclasses import fields
from datetime import date, datetime, timezone
from typing import Any, Callable, Iterable, Type, TypeAlias

from energy.logic.aggregated_consumption.exceptions import (
    IncompleteHourFiltersSet,
    InvalidHourFilteringValue, InvalidIncludeForecastValue,
    MonthPeriodStartDoesNotBeginWithFirstMonthDay,
)
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters, CommonQueryParameters,
    EnergyConsumptionQueryRawParameters, OneHourAggregationIntervalQueryParameters,
)
from energy.logic.aggregated_consumption.simple import \
    parse_str_parameter_to_int_with_correct_exception
from energy.logic.aggregated_consumption.verbose_exceptions_for_user import (
    AggregationIntervalDoesNotFitPeriod, FutureFilteringDate, InvalidHourFilteringMethod,
    PeriodStartGreaterThanEnd,
    QueryParametersInvalid, StartHourGreaterThanEndHour,
)
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
            period_end_epoch_seconds_utc=_.pop('period_end_epoch_seconds_utc'),
            period_start_epoch_seconds_utc=_.pop('period_start_epoch_seconds_utc'),
            include_forecast=_.pop('include_forecast'),
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
            period_start_epoch_seconds_utc: str,
            period_end_epoch_seconds_utc: str,
            include_forecast: str
    ):
        self.__facility_to_get_consumption_for_or_all_descendants_if_any = \
            self.__parse_facility(facility_pk_to_get_consumption_for_or_all_descendants_if_any)
        self.__aggregation_interval = aggregation_interval
        self.__set_period_boundaries(period_start_epoch_seconds_utc, period_end_epoch_seconds_utc)
        self.__include_forecast = self.__parse_include_forecast(include_forecast)
        self._validate()

    def get_parameters(self) -> CommonQueryParameters:
        return CommonQueryParameters(
            facility_to_get_consumption_for_or_all_descendants_if_any=
            self.__facility_to_get_consumption_for_or_all_descendants_if_any,
            aggregation_interval=self.__aggregation_interval,
            period_start=self._period_start,
            period_end=self._period_end,
            include_forecast=self.__include_forecast
        )

    def _validate(self):
        self.__check_period_is_valid()
        self._check_period_contains_at_least_one_aggregation_interval()

    def __set_period_boundaries(self, period_start_epoch_seconds_utc: str,
                                period_end_epoch_seconds_utc: str):
        _ = parse_str_parameter_to_int_with_correct_exception
        period_start_epoch_seconds_utc = _(period_start_epoch_seconds_utc)
        period_end_epoch_seconds_utc = _(period_end_epoch_seconds_utc)
        self._period_start = self.__convert_epoch_seconds_to_date(period_start_epoch_seconds_utc)
        self._period_end = self.__convert_epoch_seconds_to_date(period_end_epoch_seconds_utc)

    def __check_period_is_valid(self):
        if self._period_start > self._period_end:
            raise PeriodStartGreaterThanEnd

    def _check_period_contains_at_least_one_aggregation_interval(self):
        period_length_seconds = int((self._period_end - self._period_start).total_seconds())
        if period_length_seconds < self.__aggregation_interval:
            raise AggregationIntervalDoesNotFitPeriod

    def __convert_epoch_seconds_to_date(self, epoch_seconds_utc: int) -> date:
        if epoch_seconds_utc < 0:
            raise QueryParametersInvalid
        if int(time.time()) < epoch_seconds_utc:
            # future timestamp (senseless filtering for future dates)
            raise FutureFilteringDate
        return datetime.fromtimestamp(epoch_seconds_utc, timezone.utc).date()

    def __parse_facility(self, facility_pk: str) -> Facility:
        # noinspection PyTypeChecker
        return get_object_by_hashed_id_or_404(Facility, facility_pk)

    def __parse_include_forecast(self, include_forecast: str) -> bool:
        if include_forecast == 'true':
            return True
        if include_forecast == 'false':
            return False
        raise InvalidIncludeForecastValue


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
            self, *, hour_filtering_start_hour: str = None,
            hour_filtering_end_hour: str = None, hour_filtering_method: str = None,
            **kwargs
    ):
        self.__check_aggregation_interval_is_one_hour(kwargs.get('aggregation_interval'))
        self.__set_hour_filtering_options(
            hour_filtering_start_hour=hour_filtering_start_hour,
            hour_filtering_end_hour=hour_filtering_end_hour,
            hour_filtering_method=hour_filtering_method
        )
        super().__init__(**kwargs)

    def __set_hour_filtering_options(
            self, *, hour_filtering_start_hour: str,
            hour_filtering_end_hour: str, hour_filtering_method: str
    ):
        self.__hour_filtering_set = False
        hour_filters = (hour_filtering_start_hour, hour_filtering_end_hour, hour_filtering_method)
        if self.__check_all_is_not_none(hour_filters):
            self.__set_hour_filtering_parameters(
                hour_filtering_start_hour=hour_filtering_start_hour,
                hour_filtering_end_hour=hour_filtering_end_hour,
                hour_filtering_method=hour_filtering_method
            )
            return
        if self.__check_all_is_none(hour_filters):
            self.__hour_filtering_start_hour = None
            self.__hour_filtering_end_hour = None
            self.__hour_filtering_method = None
            return
        # some filter(s) is/are present while other(s) is/are not
        raise IncompleteHourFiltersSet

    def __check_all_is_not_none(self, items: Iterable) -> bool:
        return all(map(lambda x: x is not None, items))

    def __check_all_is_none(self, items: Iterable) -> bool:
        return all(map(lambda x: x is None, items))

    def get_parameters(self) -> OneHourAggregationIntervalQueryParameters:
        _ = super().get_parameters()
        base_kwargs = {field.name: getattr(_, field.name) for field in fields(_.__class__)}
        return OneHourAggregationIntervalQueryParameters(
            **base_kwargs,
            hour_filtering_start_hour=self.__hour_filtering_start_hour,
            hour_filtering_end_hour=self.__hour_filtering_end_hour,
            hour_filtering_method=self.__hour_filtering_method
        )

    def _validate(self):
        super()._validate()
        if self.__hour_filtering_set:
            self.__check_hour_filtering_range_is_correct()

    def __check_aggregation_interval_is_one_hour(self, aggregation_interval: Any):
        if aggregation_interval is not AggregationIntervalSeconds.ONE_HOUR:
            raise ValueError('this class should work only with one hour aggregation interval')

    def __check_hour_filtering_range_is_correct(self):
        if self.__hour_filtering_start_hour not in self.__HOURS:
            raise QueryParametersInvalid
        if self.__hour_filtering_end_hour not in self.__HOURS:
            raise QueryParametersInvalid
        if self.__hour_filtering_method == \
                OneHourAggregationIntervalQueryParameters.HourFilteringMethods.EVERY_DAY:
            if self.__hour_filtering_start_hour > self.__hour_filtering_end_hour:
                raise StartHourGreaterThanEndHour

    def __set_hour_filtering_parameters(
            self, hour_filtering_start_hour: str,
            hour_filtering_end_hour: str, hour_filtering_method: str):
        try:
            self.__hour_filtering_start_hour = parse_str_parameter_to_int_with_correct_exception(
                hour_filtering_start_hour
            )
            self.__hour_filtering_end_hour = parse_str_parameter_to_int_with_correct_exception(
                hour_filtering_end_hour
            )
        except QueryParametersInvalid as e:
            raise InvalidHourFilteringValue from e
        self.__set_hour_filtering_method(hour_filtering_method)
        self.__hour_filtering_set = True

    def __set_hour_filtering_method(self, hour_filtering_method: str):
        try:
            self.__hour_filtering_method = \
                OneHourAggregationIntervalQueryParameters.HourFilteringMethods(
                    hour_filtering_method
                )
        except ValueError as e:
            raise InvalidHourFilteringMethod from e


class _OneDayAggregationIntervalQueryParametersParser(__AllowQueryingForCurrentDayParser):
    pass


class __PeriodStartBeginsWithFirstDayAndPeriodEndEndsWithLastDay(_CommonQueryParametersParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _validate(self):
        super()._validate()
        self.__check_period_begins_with_first_month_day()
        self.__check_period_end_ends_with_last_month_day()

    def __check_period_begins_with_first_month_day(self):
        if self._period_start.day != 1:
            raise MonthPeriodStartDoesNotBeginWithFirstMonthDay

    def __check_period_end_ends_with_last_month_day(self):
        _, last_day = monthrange(self._period_end.year, self._period_end.month)
        if self._period_end.day != last_day:
            raise MonthPeriodStartDoesNotBeginWithFirstMonthDay


class _OneMonthAggregationIntervalQueryParametersParser(
    __PeriodStartBeginsWithFirstDayAndPeriodEndEndsWithLastDay
):
    pass


class _OneYearAggregationIntervalQueryParametersParser(_CommonQueryParametersParser):
    pass


_AGGREGATION_INTERVAL_TO_PARAMETERS_PARSER_MAPPING: \
    dict[
        AggregationIntervalSeconds,
        Type[AnyQueryParametersParser]] = \
    {
        AggregationIntervalSeconds.ONE_HOUR:  _OneHourAggregationIntervalQueryParametersParser,
        AggregationIntervalSeconds.ONE_DAY:   _OneDayAggregationIntervalQueryParametersParser,
        AggregationIntervalSeconds.ONE_WEEK:  _CommonQueryParametersParser,
        AggregationIntervalSeconds.ONE_MONTH: _OneMonthAggregationIntervalQueryParametersParser,
        AggregationIntervalSeconds.ONE_YEAR:  _OneYearAggregationIntervalQueryParametersParser
    }
