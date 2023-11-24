from django import forms
from django.utils.translation import gettext_lazy as _

from institutions.logic import common_facility_choices_format_function
from institutions.models import Facility
from utils.forms import CrispyFormsMixin, SecureModelChoiceField


class NewFacilityForm(forms.ModelForm, CrispyFormsMixin):
    # based on this field choice user will be given corresponding facilities choices
    # to set as parent for a new facility
    institution = SecureModelChoiceField(
        queryset=Facility.objects.get_institutions(),
        required=False,
        label=_("Оберіть заклад, якому буде належати об'єкт"),
        empty_label=None
    )
    # this field should be populated based on institution choice by js
    parent_facility = SecureModelChoiceField(
        queryset=Facility.objects.all(),
        required=True,
        label=_("Оберіть батьківський об'єкт"),
        widget=forms.Select(attrs={'size': 7})
    )

    class Meta:
        model = Facility
        fields = ('name', 'description')
        labels = {
            'name':        _('Назва'),
            'description': _('Опис'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        fields_order = ('institution', 'parent_facility') + fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_fields(self.Meta.fields_order)
        self.add_submit_button_at_the_end(_("Додати об'єкт"))


class FacilityEditForm(forms.ModelForm, CrispyFormsMixin):
    # info only field, qs is filled in custom method
    descendants = SecureModelChoiceField(
        queryset=Facility.objects.none(),
        label=_("Підлеглі об'єкти"),
        empty_label=None,
        required=False,
        disabled=True,
        widget=forms.Select(attrs={'size': 7}),
        # todo fix indents
        label_from_instance_function=common_facility_choices_format_function
    )
    # todo add roles that have this facility

    class Meta:
        model = Facility
        fields = ('name', 'description')
        labels = {
            'name':        _('Назва'),
            'description': _('Опис'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'institution': forms.Textarea(attrs={'rows': 1})
        }

    def fill_querysets(self, facility: Facility):
        self.fields['descendants'].queryset = facility.get_descendants()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_submit_button_at_the_end(_("Оновити"))
        # todo add delete option
