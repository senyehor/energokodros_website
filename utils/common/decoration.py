import inspect
from typing import Any, TypeGuard

from django.utils.decorators import method_decorator
from django.views import View

from utils.types import ClassView, FuncView, ViewDecorator, ViewType


def decorate_class_or_function_view(decorator: ViewDecorator) -> ViewDecorator:
    def view_wrapper(view: ViewType) -> ViewType:
        if _check_object_is_function(view):
            view = _decorate_function(view, decorator)
        elif _check_object_is_class_view(view):
            view = _decorate_class_view(view, decorator)
        else:
            raise ValueError(
                f"passed view must be a class view or function view, got type {type(view)}"
            )
        return view

    return view_wrapper


def _decorate_function(view: FuncView, decorator: ViewDecorator) -> FuncView:
    return decorator(view)


def _decorate_class_view(view: ClassView, decorator: ViewDecorator) -> ClassView:
    view.dispatch = method_decorator(decorator)(view.dispatch)
    return view


def _check_object_is_function(_object: Any) -> bool:
    return inspect.isfunction(_object)


def _check_object_is_class_view(_object: Any) -> TypeGuard[ClassView]:
    return issubclass(_object, View)
