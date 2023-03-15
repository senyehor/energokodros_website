import calendar
from datetime import datetime

from django.utils.translation import gettext as _

from energy.logic.aggregated_consumption.types import (
    FormattedConsumptionForecast, FormattedConsumptionTime, FormattedConsumptionValue,
    FormattedTotalConsumption, RawConsumptionForecast, RawConsumptionTime, RawConsumptionValue,
    RawTotalConsumption,
)


class RawAggregatedDataFormatter:
    @staticmethod
    def format_time(time: RawConsumptionTime) -> FormattedConsumptionTime:
        return time

    @staticmethod
    def format_consumption(consumption: RawConsumptionValue) -> FormattedConsumptionValue:
        return f'{consumption:.10f}'

    @staticmethod
    def format_total_consumption(total_consumption: RawTotalConsumption) \
            -> FormattedTotalConsumption:
        return f'{total_consumption:.10f}'


class OneHourFormatter(RawAggregatedDataFormatter):
    @staticmethod
    def format_time(time: datetime) -> FormattedConsumptionTime:
        # time contains start hour as we use aggregation_interval_start in select
        end_hour = str(time.hour + 1)
        return time.strftime(f'%d-%m-%Y %H:%M - {end_hour.zfill(2)}:%M')


class OneMonthFormatter(RawAggregatedDataFormatter):
    @staticmethod
    def format_time(time: str) -> FormattedConsumptionTime:
        def __get_year_and_month_from_time(_time: str) -> tuple[str, str]:
            parts = _time.split('-')
            return parts[0], parts[1]

        def __get_month_name(month_number_from_zero: int) -> str:
            return _(calendar.month_name[month_number_from_zero])

        year, month = __get_year_and_month_from_time(time)
        month_name = __get_month_name(int(month))
        return f'{year} {month_name}'


def format_forecast(forecast: RawConsumptionForecast) -> FormattedConsumptionForecast:
    return f'{forecast:.10f}'
