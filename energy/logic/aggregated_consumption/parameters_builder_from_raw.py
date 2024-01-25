from typing import Type

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import (
    AnyQueryParameters,
    EnergyConsumptionQueryRawParameters,
)
from energy.logic.aggregated_consumption.parameters_parsers import AnyParametersParser
from institutions.models import Facility


class ParametersBuilder:
    __PARAMETERS_PASSED_MANUALLY = ('role', 'facility', 'aggregation_interval_seconds')

    def __init__(
            self, facility_to_get_consumption_for_or_all_descendants_if_any: Facility,
            aggregation_interval: AggregationIntervalSeconds,
            raw_parameters: EnergyConsumptionQueryRawParameters
    ):
        self.__facility = facility_to_get_consumption_for_or_all_descendants_if_any
        self.__aggregation_interval = aggregation_interval
        self.__raw_parameters = raw_parameters

    def compose_parameters(self, parser: Type[AnyParametersParser]) -> AnyQueryParameters:
        dynamic_parameters = self.__exclude_already_parsed_parameters()
        return parser(
            facility_to_get_consumption_for_or_all_descendants_if_any=self.__facility,
            aggregation_interval=self.__aggregation_interval,
            **dynamic_parameters
        ).get_parameters()

    def __exclude_already_parsed_parameters(self) -> dict[str, str]:
        return {
            key: value for key, value in self.__raw_parameters.items()
            if key not in self.__PARAMETERS_PASSED_MANUALLY
        }
