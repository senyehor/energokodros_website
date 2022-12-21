from django.http import HttpRequest

from users.logic.simple import get_applications_from_users_who_confirmed_email
from utils.common import is_admin_non_authenticated_safe


def user_roles_applications_to_review_count(request: HttpRequest) -> dict:
    if is_admin_non_authenticated_safe(request.user):
        count = get_applications_from_users_who_confirmed_email().count()
        return {
            'users_roles_applications_count': count
        }
    return {}
