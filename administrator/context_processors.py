from administrator.logic import _get_applications_from_users_who_confirmed_email_ordered, _is_admin


def user_roles_applications_to_review_count(request):
    if _is_admin(request):
        return {
            'users_roles_applications_count':
                _get_applications_from_users_who_confirmed_email_ordered().count()
        }
    return None
