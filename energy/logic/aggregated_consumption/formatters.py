import calendar
from datetime import datetime
from typing import TypeAlias

from django.utils.translation import gettext as _

from energy.logic.aggregated_consumption.types import (
    AggregatedConsumptionData, ConsumptionForecast, ConsumptionTime, ConsumptionValue,
    FormattedConsumptionForecast,
    FormattedConsumptionTime,
    FormattedConsumptionValue, RawAggregatedConsumptionDataWithForecast,
)


class CommonFormatter:
    def format(self, raw_consumption_with_forecast: RawAggregatedConsumptionDataWithForecast) \
            -> AggregatedConsumptionData:
        return [
            (
                self._format_time(time),
                self._format_consumption(consumption),
                self._format_forecast(forecast)
            )
            for time, consumption, forecast in raw_consumption_with_forecast
        ]

    def _format_time(self, time: ConsumptionTime) -> FormattedConsumptionTime:
        return time

    def _format_consumption(self, consumption: ConsumptionValue) -> FormattedConsumptionValue:
        return f'{consumption:.10f}'

    def _format_forecast(self, forecast: ConsumptionForecast) -> FormattedConsumptionForecast:
        return f'{forecast:.10f}'


class OneHourFormatter(CommonFormatter):
    def _format_time(self, time: datetime) -> FormattedConsumptionTime:
        # time contains start hour as we use aggregation_interval_start in select
        end_hour = str(time.hour + 1)
        return time.strftime(f'%d-%m-%Y %H:%M - {end_hour.zfill(2)}:%M')


class OneMonthFormatter(CommonFormatter):
    def _format_time(self, time: str) -> FormattedConsumptionTime:
        year, month = self.__get_year_and_month_from_time(time)
        month_name = self.__get_month_name(int(month))
        return f'{year} {month_name}'

    def __get_year_and_month_from_time(self, time: str) -> tuple[str, str]:
        parts = time.split('-')
        return parts[0], parts[1]

    def __get_month_name(self, month_number_from_zero: int) -> str:
        return _(calendar.month_name[month_number_from_zero])


AnyFormatter: TypeAlias = 'CommonFormatter'
