from datetime import datetime
from typing import Callable

from energy.logic.aggregated_consumption.formatters import format_forecast
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import AnyQueryParameters
from energy.logic.aggregated_consumption.simple import check_institution_is_kindergarten_28
from energy.logic.aggregated_consumption.types import (
    ConsumptionForecast, ConsumptionForecastRawAndFormatted, ConsumptionRawAndFormatted,
    ConsumptionRawAndFormattedWithForecastRawAndFormatted,
    ConsumptionRecordRawAndFormattedWithRawAndFormattedForecast, ConsumptionRecordWithForecastForIt,
    ConsumptionWithConsumptionForecast,
    RawConsumptionForecast,
    RawConsumptionTime,
)
from energy.logic.aggregated_consumption.verbose_exceptions_for_user import \
    ForecastForParametersDoesNotExist


class ConsumptionForecaster:
    """
    currently this is just a stub returning hardcoded data,
    but will be a forecasting AI
    """
    __format_forecast: Callable[[RawConsumptionForecast], ConsumptionForecast] = \
        staticmethod(format_forecast)

    def __init__(
            self, parameters: AnyQueryParameters,
            raw_and_formatted_consumption: ConsumptionRawAndFormatted
    ):
        self.__parameters = parameters
        self.__raw_and_formatted_consumption = raw_and_formatted_consumption

    def get_consumption_with_forecast(self) -> ConsumptionWithConsumptionForecast:
        self.__check_forecast_is_available_for_parameters()
        return (
            ConsumptionRecordWithForecastForIt(
                time=record.formatted_consumption_record.time,
                value=record.formatted_consumption_record.value,
                forecast=self.__format_forecast(
                    self.__get_forecast_for_date(record.raw_consumption_record.time)
                ),
            )
            for record in self.__raw_and_formatted_consumption
        )

    def get_raw_and_formatted_consumption_with_raw_and_formatted_forecast(self) -> \
            ConsumptionRawAndFormattedWithForecastRawAndFormatted:
        self.__check_forecast_is_available_for_parameters()
        return [
            ConsumptionRecordRawAndFormattedWithRawAndFormattedForecast(
                raw_consumption_record=record.raw_consumption_record,
                formatted_consumption_record=record.formatted_consumption_record,
                forecast_raw_and_formatted=ConsumptionForecastRawAndFormatted(
                    raw=raw_forecast,
                    formatted=self.__format_forecast(raw_forecast)
                )
            )
            for record in self.__raw_and_formatted_consumption
            # trick to avoid double raw forecast retrieval while creating
            # forecast_raw_and_formatted, as "if" condition is always true,
            # but creates raw_forecast
            if (raw_forecast := self.__get_forecast_for_date(record.raw.time)) and record
        )

    def __get_forecast_for_date(self, date: RawConsumptionTime) -> RawConsumptionForecast:
        return self.__get_forecast_for_kindergarten(date)

    def __get_forecast_for_kindergarten(self, date: datetime) -> RawConsumptionForecast:
        is_workday = self.__check_day_is_workday(date.weekday())
        if self.__parameters.aggregation_interval == AggregationIntervalSeconds.ONE_HOUR:
            hour = date.hour
            return self.__get_forecast_for_hour_for_kindergarten(is_workday, hour)
        if self.__parameters.aggregation_interval == AggregationIntervalSeconds.ONE_DAY:
            if is_workday:
                return KINDERGARTEN_CONSUMPTION_PER_WORKDAY
            return KINDERGARTEN_CONSUMPTION_PER_WEEKEND_DAY
        # double-checking parameters are correct
        raise ForecastForParametersDoesNotExist

    def __check_forecast_is_available_for_parameters(self):
        facility_is_kindergarten = self.__check_facility_is_kindergarten()
        interval_is_one_hour_or_one_day = self.__check_aggregation_interval_is_one_hour_or_one_day()
        if facility_is_kindergarten and interval_is_one_hour_or_one_day:
            return
        raise ForecastForParametersDoesNotExist

    def __check_aggregation_interval_is_one_hour_or_one_day(self) -> bool:
        one_hour = self.__parameters.aggregation_interval == AggregationIntervalSeconds.ONE_HOUR
        one_day = self.__parameters.aggregation_interval == AggregationIntervalSeconds.ONE_DAY
        return one_hour or one_day

    def __check_facility_is_kindergarten(self) -> bool:
        """forecast is only available for kindergarten 28"""
        return check_institution_is_kindergarten_28(
            self.__parameters.facility_to_get_consumption_for_or_all_descendants_if_any
        )

    def __get_forecast_for_hour_for_kindergarten(
            self, is_workday: bool, interval_start_hour_0_to_23: int
    ) -> RawConsumptionForecast:
        if is_workday:
            forecast_source = \
                KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WORKDAY_BY_START_HOUR
        else:
            forecast_source = \
                KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WEEKEND_BY_START_HOUR
        return forecast_source[interval_start_hour_0_to_23]

    def __check_day_is_workday(self, day_number_from_zero: int) -> bool:
        return day_number_from_zero in range(5)


KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WORKDAY_BY_START_HOUR = {
    0:  1.57,
    1:  1.57,
    2:  1.57,
    3:  1.57,
    4:  1.57,
    5:  1.57,
    6:  1.57,
    7:  18.412,
    8:  24.283,
    9:  48.1394,
    10: 47.7198,
    11: 20.7058,
    12: 20.5874,
    13: 21.704,
    14: 21.663,
    15: 18.3154,
    16: 19.4908,
    17: 10.0008,
    18: 10.8984,
    19: 7.2084,
    20: 2.69,
    21: 1.57,
    22: 1.57,
    23: 1.57
}

KINDERGARTEN_CONSUMPTION_PER_WORKDAY = sum(
    KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WORKDAY_BY_START_HOUR.values()
)

KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WEEKEND_BY_START_HOUR = {
    0:  1.57,
    1:  1.57,
    2:  1.57,
    3:  1.57,
    4:  1.57,
    5:  1.57,
    6:  1.57,
    7:  1.682,
    8:  1.682,
    9:  1.682,
    10: 1.682,
    11: 1.682,
    12: 1.682,
    13: 1.682,
    14: 1.682,
    15: 1.682,
    16: 1.682,
    17: 1.682,
    18: 1.682,
    19: 2.802,
    20: 2.690,
    21: 1.57,
    22: 1.57,
    23: 1.57
}

KINDERGARTEN_CONSUMPTION_PER_WEEKEND_DAY = sum(
    KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WEEKEND_BY_START_HOUR.values()
)
