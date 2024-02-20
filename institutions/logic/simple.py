from django.db.models import QuerySet

from institutions.models import Facility
from users.models import UserRole


def label_from_user_role_for_facility_roles(role: UserRole) -> str:
    return f'{role.user.full_name}, {role.position_name}'


def get_all_facilities_of_facility_institution(facility: Facility):
    return facility.get_tree(facility.get_institution())


def get_all_descendants_of_facility_with_self(facility: Facility) -> QuerySet:
    return facility.get_tree(facility)
