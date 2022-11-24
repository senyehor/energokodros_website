from users.logic.simple import get_applications_from_users_who_confirmed_email
from utils.common.admin_rights import is_admin


def user_roles_applications_to_review_count(request):
    if is_admin(request):
        count = get_applications_from_users_who_confirmed_email().count()
        return {
            'users_roles_applications_count': count
        }
    return {}
