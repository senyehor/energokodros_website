from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import HttpRequest

from institutions.models import Facility
from users.models import User, UserRole, UserRoleApplication


def check_role_belongs_to_user(user: User, user_role: UserRole):
    if user_role.user != user:
        raise PermissionDenied
    return True


def check_role_has_access_for_facility(user_role: UserRole, facility: Facility):
    if user_role.facility_has_access_to == facility:
        return
    if facility.is_descendant_of(user_role.facility_has_access_to):
        return
    raise PermissionDenied


def remember_user_for_two_week(request: HttpRequest):
    __remember_user_for_timedelta(request, timedelta(weeks=2))


def check_user_has_no_roles(user: User) -> bool:
    return not user.roles.exists()


def get_applications_from_users_who_confirmed_email() -> QuerySet:
    return UserRoleApplication.objects.filter(user__is_active=True)


def get_users_with_confirmed_email() -> QuerySet:
    return User.objects.filter(is_active=True)


def __remember_user_for_timedelta(request: HttpRequest, td: timedelta):
    request.session.set_expiry(td)
