from datetime import datetime, timedelta
from decimal import Decimal

from django.db import connection

from energy.logic.aggregated_energy_consumption_query_builder import (
    EnergyConsumptionQueryBuilder, EnergyConsumptionQueryParameters,
)
from institutions.models import Facility


class AggregatedEnergyConsumptionController:
    def __init__(
            self, period_start_epoch: int, period_end_epoch: int,
            aggregation_interval_seconds: int,
            facility_to_get_consumption_for_or_all_descendants_if_any: Facility
    ):
        # todo think of adding error messages
        self.__period_start_epoch = period_start_epoch
        self.__period_end_epoch = period_end_epoch
        self.__aggregation_interval_seconds = aggregation_interval_seconds
        self.__facility = facility_to_get_consumption_for_or_all_descendants_if_any
        self.__validate_and_make_params()

    def __validate_and_make_params(self):
        # todo add adequate epoch check
        if self.__period_start_epoch < 0 \
                or self.__period_end_epoch < 0 \
                or self.__aggregation_interval_seconds < 0:
            raise InvalidDataProvided('negative numbers are not allowed')
        period_start = datetime.fromtimestamp(self.__period_start_epoch).date()
        period_end = datetime.fromtimestamp(self.__period_end_epoch).date()
        aggregation_interval = timedelta(seconds=self.__aggregation_interval_seconds)
        # todo add exception handling
        self.__params = EnergyConsumptionQueryParameters(
            period_start, period_end, aggregation_interval, self.__facility
        )

    def get_consumption(self) -> list[tuple[str, Decimal]]:
        # todo type
        query = EnergyConsumptionQueryBuilder.build_query(self.__params)
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


class InvalidDataProvided(ValueError):
    pass
