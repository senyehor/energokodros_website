import functools

from django.http import HttpRequest, QueryDict
from django.shortcuts import render

from energy.logic.aggregated_consumption.exceptions import QueryParametersInvalid
from users.logic import check_user_has_no_roles
from utils.types import FuncView, StrStrDict


def convert_request_post_dict_to_regular_dict(post_dict: QueryDict) -> StrStrDict:
    return post_dict.dict()


def parse_str_parameter_to_int_with_correct_exception(value: str) -> int:
    try:
        return int(value)
    except ValueError as e:
        raise QueryParametersInvalid from e


def parse_include_forecast_parameter(include_forecast: str) -> bool:
    if include_forecast == 'true':
        return True
    if include_forecast == 'false':
        return False
    raise QueryParametersInvalid('include_forecast must be true or false')


def show_no_roles_page_if_user_has_no_roles(view: FuncView) -> FuncView:
    @functools.wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if check_user_has_no_roles(request.user):
            return render(request, 'energy/consumption/you_have_no_roles.html')
        return view(request, *args, **kwargs)

    return wrapper
