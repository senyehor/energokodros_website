from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from institutions.models import Facility
from utils.forms import CrispyFormsMixin, SecureModelChoiceField


class NewFacilityForm(ModelForm, CrispyFormsMixin):
    # based on this field choice user will be given corresponding facilities choices
    # to set as parent for a new facility
    institution = SecureModelChoiceField(
        queryset=Facility.objects.get_institutions(),
        required=False,
        label=_("Оберіть заклад, якій буде належати об'єкт"),
        empty_label=None
    )
    # this field should be populated based on institution choice by js
    parent_facility = SecureModelChoiceField(
        queryset=Facility.objects.all(),
        required=True,
        label=_("Оберіть батьківський об'єкт"),
    )

    class Meta:
        model = Facility
        fields = ('name', 'description')
        labels = {
            'name':        _('Назва'),
            'description': _('Опис'),
        }
        widgets = {
            'description': Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_submit_button_at_the_end(_("Додати об'єкт"))
