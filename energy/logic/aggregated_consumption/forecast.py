import os
from datetime import datetime

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import AnyQueryParameters
from energy.logic.aggregated_consumption.types import (
    ConsumptionForecast, ConsumptionTime, RawAggregatedConsumptionData,
    RawAggregatedConsumptionDataWithForecast,
)
from institutions.models import Facility


class ConsumptionForecaster:
    """
    currently this is just a stub returning hardcoded data,
    but will be a forecasting AI
    """

    def __init__(self, parameters: AnyQueryParameters, consumption: RawAggregatedConsumptionData):
        self.__parameters = parameters
        self.__consumption = consumption

    def get_consumption_forecast(self) -> RawAggregatedConsumptionDataWithForecast:
        return [
            (
                date,
                consumption,
                self.__get_forecast_for_date(date)
            )
            for date, consumption in self.__consumption
        ]

    def __get_forecast_for_date(self, date: ConsumptionTime) -> ConsumptionForecast:
        if self.__check_is_kindergarten_and_interval_is_one_hour():
            return self.__get_forecast_for_kindergarten(date)
        return 0

    def __get_forecast_for_kindergarten(self, date: datetime) -> ConsumptionForecast:
        day_number = date.weekday()
        hour = date.hour
        forecast_source = self.__get_forecast_source_for_kindergarten(
            self.__check_day_is_working(day_number)
        )
        return forecast_source[hour]

    def __check_is_kindergarten_and_interval_is_one_hour(self) -> bool:
        is_kindergarten = self.__check_facility_is_kindergarten()
        interval_is_one_day = self.__check_aggregation_interval_is_one_hour()
        return is_kindergarten and interval_is_one_day

    def __check_aggregation_interval_is_one_hour(self) -> bool:
        return self.__parameters.aggregation_interval == AggregationIntervalSeconds.ONE_HOUR

    def __check_facility_is_kindergarten(self) -> bool:
        return self.__parameters.facility_to_get_consumption_for_or_all_descendants_if_any == \
            Facility.objects.get(pk=os.getenv('KINDERGARTEN_ID'))

    def __get_forecast_source_for_kindergarten(self, is_day_working: bool) \
            -> dict[int, ConsumptionForecast]:
        if is_day_working:
            return KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WORKING_DAY_BY_HOUR
        return KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WEEKEND_BY_HOUR

    def __check_day_is_working(self, day_number_from_zero: int) -> bool:
        return day_number_from_zero in range(5)


KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WORKING_DAY_BY_HOUR = {
    0:  0.1,
    1:  0.1,
    2:  0.2,
    3:  0.3,
    4:  0.4,
    5:  0.5,
    6:  0.6,
    7:  0.7,
    8:  0.8,
    9:  0.9,
    10: 0.10,
    11: 0.11,
    12: 0.12,
    13: 0.13,
    14: 0.14,
    15: 0.15,
    16: 0.16,
    17: 0.17,
    18: 0.18,
    19: 0.19,
    20: 0.20,
    21: 0.21,
    22: 0.22,
    23: 0.23
}

KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WEEKEND_BY_HOUR = {
    0:  0,
    1:  0.1,
    2:  0.2,
    3:  0.3,
    4:  0.4,
    5:  0.5,
    6:  0.6,
    7:  0.7,
    8:  0.8,
    9:  0.9,
    10: 0.10,
    11: 0.11,
    12: 0.12,
    13: 0.13,
    14: 0.14,
    15: 0.15,
    16: 0.16,
    17: 0.17,
    18: 0.18,
    19: 0.19,
    20: 0.20,
    21: 0.21,
    22: 0.22,
    23: 0.23
}
