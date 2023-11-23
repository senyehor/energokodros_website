from django.db.models import QuerySet
from django.http import HttpRequest

from users.models import User, UserRoleApplication


def check_user_has_no_roles(user: User) -> bool:
    return not user.roles.exists()


def get_applications_from_users_who_confirmed_email() -> QuerySet:
    return UserRoleApplication.objects.filter(user__is_active=True)


def get_users_with_confirmed_email() -> QuerySet:
    return User.objects.filter(is_active=True)


def is_admin(request: HttpRequest) -> bool:
    return request.user.is_authenticated and request.user.is_admin  # noqa
