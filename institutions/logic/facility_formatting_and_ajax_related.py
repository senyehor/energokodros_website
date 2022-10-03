from builtins import tuple

from django.shortcuts import get_object_or_404
from django.utils.safestring import mark_safe

from institutions.models import Facility
from utils.forms import _reveal_id, SecureModelChoiceField  # noqa


def compose_formatted_institution_facilities_choices(
        institution: Facility) -> list[tuple[str, str]]:
    if not institution.is_root():
        raise ValueError('provided objects is a facility, not institution')
    choices = SecureModelChoiceFieldWithVerboseFacilityLabeling(
        queryset=Facility.objects.get_all_institution_objects(institution),
        empty_label=None
    ).choices
    return [(str(value), label) for value, label in choices]


def get_institution_by_hashed_id(hashed_institution_id: str) -> Facility:
    return get_object_or_404(
        Facility,
        pk=_reveal_id(hashed_institution_id)
    )


class SecureModelChoiceFieldWithVerboseFacilityLabeling(SecureModelChoiceField):
    def label_from_instance(self, obj: Facility):
        if not isinstance(obj, Facility):
            raise ValueError('provided object is not a facility')
        # &nbsp; is one space equivalent that is correctly rendered in html form
        return mark_safe('&nbsp;&nbsp;' * (obj.depth - 1) + obj.name)
