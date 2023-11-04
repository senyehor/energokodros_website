from django.http import QueryDict

from energy.logic.aggregated_consumption.exceptions import QueryParametersInvalid
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import EnergyConsumptionQueryRawParameters


def convert_request_post_dict_to_raw_parameters(
        post_dict: QueryDict) -> EnergyConsumptionQueryRawParameters:
    return EnergyConsumptionQueryRawParameters(**post_dict.dict())


def parse_aggregation_interval(aggregation_interval: str) -> AggregationIntervalSeconds:
    try:
        aggregation_interval_seconds = parse_str_parameter_to_int_with_correct_exception(
            aggregation_interval
        )
        return AggregationIntervalSeconds(aggregation_interval_seconds)
    except ValueError as e:
        raise QueryParametersInvalid from e


def parse_str_parameter_to_int_with_correct_exception(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise QueryParametersInvalid from e
