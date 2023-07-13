from administrator.logic.helper_functions import (
    get_applications_from_users_who_confirmed_email_ordered,
    is_admin,
)


def user_roles_applications_to_review_count(request):
    if is_admin(request):
        _ = get_applications_from_users_who_confirmed_email_ordered()
        return {
            'users_roles_applications_count': _.count()
        }
    return {}
