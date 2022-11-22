from django.utils.safestring import mark_safe

from institutions.models import Facility
from utils.common import compose_secure_choices_for_queryset
from utils.common.model_objects_crypto_related import Choices


def common_facility_choices_format_function(facility: Facility):
    return mark_safe('&nbsp;&nbsp;' * (facility.depth - 1) + facility.name)


def compose_formatted_institution_facilities_choices(institution: Facility) -> Choices:
    if not institution.is_root():
        raise ValueError('provided objects is a facility, not institution')
    return compose_formatted_facility_descendants_and_itself(institution)


def compose_formatted_facility_descendants_and_itself(facility: Facility) -> Choices:
    return compose_secure_choices_for_queryset(
        facility.get_tree(facility),
        common_facility_choices_format_function
    )
