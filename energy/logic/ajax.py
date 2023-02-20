from institutions.logic import \
    make_facility_and_descendants_choices_with_padding_according_to_nesting
from users.models import UserRole
from utils.common import Choices


def get_facilities_formatted_choices_for_user_role(role: UserRole) -> Choices:
    return make_facility_and_descendants_choices_with_padding_according_to_nesting(
        role.facility_has_access_to
        )
