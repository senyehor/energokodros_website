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

KINDERGARTEN_CONSUMPTION_FORECAST_KILOWATT_HOUR_FOR_WEEKEND_BY_HOUR = {
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
