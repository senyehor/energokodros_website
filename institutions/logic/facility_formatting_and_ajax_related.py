from builtins import tuple
from typing import TypeAlias

from django.db.models import QuerySet
from django.utils.safestring import mark_safe

from institutions.models import Facility
from utils.forms import SecureModelChoiceField

Choices: TypeAlias = list[tuple[str, str]]


def compose_formatted_institution_facilities_choices(institution: Facility) -> Choices:
    if not institution.is_root():
        raise ValueError('provided objects is a facility, not institution')
    return __compose_choices_for_queryset(Facility.objects.get_all_institution_objects(institution))


def compose_formatted_facility_descendants_and_itself(facility: Facility) -> Choices:
    return __compose_choices_for_queryset(facility.get_tree(facility))


def __compose_choices_for_queryset(qs: QuerySet) -> Choices:
    choices = SecureModelChoiceFieldWithVerboseFacilityLabeling(
        queryset=qs,
        empty_label=None
    ).choices
    return [(str(value), label) for value, label in choices]


class SecureModelChoiceFieldWithVerboseFacilityLabeling(SecureModelChoiceField):
    def label_from_instance(self, obj: Facility):
        if not isinstance(obj, Facility):
            raise ValueError('provided object is not a facility')
        # &nbsp; is one space equivalent that is correctly rendered in html form
        return mark_safe('&nbsp;&nbsp;' * (obj.depth - 1) + obj.name)
