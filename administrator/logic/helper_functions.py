from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from users.models import User, UserRoleApplication


def get_message_for_role_application(application_id: int) -> UserRoleApplication:
    # as we use SecureModelChoiceField we get request_id hashed,
    # so converting it to int back
    return get_object_or_404(UserRoleApplication, pk=application_id)


def check_user_has_no_roles(user: User) -> bool:
    return not user.roles.exists()


def get_applications_from_users_who_confirmed_email_ordered() -> QuerySet:
    return UserRoleApplication.objects.all().filter(user__is_active=True).order_by('-pk')


def is_admin(request: HttpRequest):
    return request.user.is_authenticated and request.user.is_admin  # noqa
