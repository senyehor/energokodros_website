import functools

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from users.models import User
from utils.common.decoration import decorate_class_or_function_view
from utils.types import FuncView, ViewType


def admin_rights_and_login_required(view: ViewType):
    return decorate_class_or_function_view(_admin_rights_and_login_required)(view)


def _admin_rights_and_login_required(view: FuncView) -> FuncView:
    view = login_required(view)
    view = _admin_rights_required(view)
    return view


def _admin_rights_required(view: FuncView) -> FuncView:
    @functools.wraps(view)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if is_admin_non_authenticated_safe(request.user):
            return view(request, *args, **kwargs)
        return HttpResponse(status=403)

    return wrapper


def is_admin_non_authenticated_safe(user: User) -> bool:
    return user.is_authenticated and user.is_admin
