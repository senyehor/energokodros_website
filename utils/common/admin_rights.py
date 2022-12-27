import functools
import inspect
from typing import Type

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from energokodros.settings import LOGIN_URL
from users.models import User
from utils.types import FuncView, View


def admin_rights_required(obj_to_decorate: View) -> View:
    if inspect.isfunction(obj_to_decorate):
        return __admin_right_required_function_decorator(obj_to_decorate)
    return __admin_right_required_class_decorator(obj_to_decorate)


def __admin_right_required_class_decorator(_class: View) -> View:
    _class.dispatch = method_decorator(__admin_right_required_function_decorator)(_class.dispatch)
    return _class


def __admin_right_required_function_decorator(function: FuncView) -> Type[FuncView]:
    @functools.wraps(function)
    def _wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(LOGIN_URL)
        if request.user.is_admin:
            return function(request, *args, **kwargs)
        return HttpResponse(status=403)

    return _wrapper


def is_admin_non_authenticated_safe(user: User) -> bool:
    return user.is_authenticated and user.is_admin
