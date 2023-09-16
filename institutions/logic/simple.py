from django.shortcuts import get_object_or_404

from institutions.models import Facility
from utils.forms import SecureModelChoiceField


def compose_formatted_institution_facilities_choices(institution: Facility) -> dict[str, str]:
    if not institution.is_root():
        raise ValueError('provided objects is a facility, not institution')
    choices = __FormattedSecureModelChoiceField(
        queryset=Facility.objects.get_all_institution_objects(institution),
        empty_label=None
    ).choices
    return {str(value): label for value, label in choices}


class __FormattedSecureModelChoiceField(SecureModelChoiceField):
    def label_from_instance(self, obj: Facility):
        # &nbsp; is one space equivalent that is correctly rendered in html form
        return '&nbsp;&nbsp;' * (obj.depth - 1) + str(obj)


def get_institution_by_hashed_id(hashed_institution_id: str) -> Facility:
    return get_object_or_404(
        Facility,
        pk=SecureModelChoiceField._reveal_id(hashed_institution_id)  # noqa pylint: disable=W0212
    )
