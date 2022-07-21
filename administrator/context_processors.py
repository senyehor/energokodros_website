from administrator.logic import (
    get_applications_from_users_who_confirmed_email,
    is_admin,
)


def user_roles_applications_to_review_count(request):
    if is_admin(request):
        _ = get_applications_from_users_who_confirmed_email()
        return {
            'users_roles_applications_count': _.count()
        }
    return {}
