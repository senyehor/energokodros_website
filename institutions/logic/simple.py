from users.models import UserRole


def label_from_user_role_for_facility_roles(role: UserRole) -> str:
    return f'{role.user.full_name}, {role.position_name}'