from institutions.logic import compose_formatted_facility_descendants_and_itself
from users.models import UserRole
from utils.common import Choices


def get_facilities_formatted_choices_for_user_role(role: UserRole) -> Choices:
    return compose_formatted_facility_descendants_and_itself(role.facility_has_access_to)
