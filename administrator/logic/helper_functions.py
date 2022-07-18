from django.db.models import QuerySet
from django.http import HttpRequest

from users.models import User, UserRoleApplication
from utils.common import all_object_pk_ordered


def check_user_has_no_roles(user: User) -> bool:
    return not user.roles.exists()


def get_applications_from_users_who_confirmed_email_ordered() -> QuerySet:
    return all_object_pk_ordered(UserRoleApplication).filter(user__is_active=True)


def is_admin(request: HttpRequest) -> bool:
    return request.user.is_authenticated and request.user.is_admin  # noqa
