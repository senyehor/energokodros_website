import functools

from django.http import HttpRequest, QueryDict
from django.shortcuts import render

from energy.logic.aggregated_consumption.exceptions import QueryParametersInvalid
from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from energy.logic.aggregated_consumption.parameters import EnergyConsumptionQueryRawParameters
from users.logic import check_user_has_no_roles
from utils.types import FuncView


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


def show_no_roles_page_if_user_has_no_roles(view: FuncView) -> FuncView:
    @functools.wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if check_user_has_no_roles(request.user):
            return render(request, 'energy/consumption/you_have_no_roles.html')
        return view(request, *args, **kwargs)

    return wrapper
