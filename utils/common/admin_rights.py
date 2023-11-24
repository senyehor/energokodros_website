import functools
import inspect
from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View


def admin_rights_required(obj_to_decorate: Callable | View) -> Callable | View:
    if inspect.isfunction(obj_to_decorate):
        return __admin_right_required_function_decorator(obj_to_decorate)
    return __admin_right_required_class_decorator(obj_to_decorate)


def __admin_right_required_class_decorator(_class: View) -> View:
    _class.dispatch = method_decorator(__admin_right_required_function_decorator)(_class.dispatch)
    return _class


def __admin_right_required_function_decorator(function: Callable) -> Callable:
    @functools.wraps(function)
    def _wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and is_admin:
            return function(request, *args, **kwargs)
        return HttpResponse(status=403)

    return _wrapper


def is_admin(request: HttpRequest) -> bool:
    return request.user.is_authenticated and request.user.is_admin  # noqa
