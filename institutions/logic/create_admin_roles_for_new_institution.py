from institutions.models import Facility
from users.models import User, UserRole

__ADMIN_ROLE_NAME = 'Роль адміністратора'


def create_admin_roles_for_new_institution(institution: Facility):
    admins = User.objects.filter(is_admin=True)
    for admin in admins:
        UserRole(
            user=admin,
            facility_has_access_to=institution,
            position_name=__ADMIN_ROLE_NAME
        ).save()
