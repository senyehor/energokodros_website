from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from institutions.models import Facility
from users.models import User, UserRole


def check_role_belongs_to_user(user: User, user_role: UserRole):
    if user_role.user != user:
        raise PermissionDenied


def check_role_has_access_for_facility(user_role: UserRole, facility: Facility):
    if user_role.facility_has_access_to.is_descendant_of(facility):
        return
    if user_role.facility_has_access_to == facility:
        return
    raise PermissionDenied


def remember_user_for_two_week(request: HttpRequest):
    __remember_user_for_timedelta(request, timedelta(weeks=2))


def __remember_user_for_timedelta(request: HttpRequest, td: timedelta):
    request.session.set_expiry(td)


def format_user_role(role: UserRole) -> str:
    return _(f"{role.position_name}, об'єкт {role.facility_has_access_to.name}")
