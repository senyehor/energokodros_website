from django.utils.safestring import mark_safe

from institutions.models import Facility
from utils.common import compose_secure_choices_for_queryset
from utils.common.model_objects_crypto_related import Choices


def get_facility_name_space_padded_according_to_nesting(facility: Facility) -> str:
    return mark_safe('&nbsp;&nbsp;' * (facility.depth - 1) + facility.name)


def make_institution_facilities_choices_with_padding_according_to_nesting(institution: Facility) \
        -> Choices:
    if not institution.is_root():
        raise ValueError('provided objects is a facility, not institution')
    return make_facility_and_descendants_choices_with_padding_according_to_nesting(institution)


def make_facility_and_descendants_choices_with_padding_according_to_nesting(facility: Facility) \
        -> Choices:
    return compose_secure_choices_for_queryset(
        facility.get_tree(facility),
        get_facility_name_space_padded_according_to_nesting
    )
