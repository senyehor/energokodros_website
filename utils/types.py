from typing import Any, Callable, Tuple, TypeAlias

from django.http import HttpRequest, HttpResponse
from django.views import View as View_for_typehint

StrTuple: TypeAlias = Tuple[str, ...]
StrKeyDict: TypeAlias = dict[str, Any]
FuncView: TypeAlias = Callable[[HttpRequest, ...], HttpResponse]
ClassView: TypeAlias = View_for_typehint
ViewType: TypeAlias = FuncView | ClassView
ViewDecorator: TypeAlias = Callable[[ViewType], ViewType]
