from django.utils.safestring import mark_safe

from institutions.models import Facility
from utils.common import compose_choices_for_queryset
from utils.common.model_objects_crypto_related import Choices
from utils.forms import SecureModelChoiceField


def compose_formatted_institution_facilities_choices(institution: Facility) -> Choices:
    if not institution.is_root():
        raise ValueError('provided objects is a facility, not institution')
    return compose_formatted_facility_descendants_and_itself(institution)


def compose_formatted_facility_descendants_and_itself(facility: Facility) -> Choices:
    return compose_choices_for_queryset(
        facility.get_tree(facility),
        SecureModelChoiceFieldWithVerboseFacilityLabeling
    )


class SecureModelChoiceFieldWithVerboseFacilityLabeling(SecureModelChoiceField):
    def label_from_instance(self, obj: Facility):
        if not isinstance(obj, Facility):
            raise ValueError('provided object is not a facility')
        # &nbsp; is one space equivalent that is correctly rendered in html form
        return mark_safe('&nbsp;&nbsp;' * (obj.depth - 1) + obj.name)
