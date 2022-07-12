import functools
from types import FunctionType

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View


def admin_rights_required(obj_to_decorate: FunctionType | View):
    if isinstance(obj_to_decorate, FunctionType):
        return __admin_right_required_function_decorator(obj_to_decorate)
    return __admin_right_required_class_decorator(obj_to_decorate)


def __admin_right_required_class_decorator(_class: View):
    _class.dispatch = method_decorator(__admin_right_required_function_decorator)(_class.dispatch)
    return _class


def __admin_right_required_function_decorator(function: FunctionType):
    @functools.wraps(function)
    def _wrapper(request, *args, **kwargs):
        return function(request, *args, **kwargs) \
            if request.user.is_authenticated and request.user.is_admin \
            else HttpResponse(status=403)

    return _wrapper
