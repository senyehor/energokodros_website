from django import forms
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from institutions.logic import (
    common_facility_choices_format_function,
    label_from_user_role_for_facility_roles,
)
from institutions.models import Facility
from users.models import UserRole
from utils.forms import (
    create_primary_button, CrispyFormsMixin, SecureModelChoiceField,
    SelectWithFormControlClass, UPDATE_DELETE_BUTTONS_SET,
)
from utils.views import AdditionalSetupRequiredFormMixin


class NewFacilityForm(CrispyFormsMixin, forms.ModelForm):
    # based on this field choice user will be given corresponding facilities choices
    # to set as parent for a new facility
    institution = SecureModelChoiceField(
        queryset=Facility.objects.get_institutions(),
        required=False,
        label=_("Оберіть заклад, якому буде належати об'єкт"),
        empty_label=None,
        widget=SelectWithFormControlClass(),
    )
    # this field should be populated based on institution choice by js
    parent_facility = SecureModelChoiceField(
        queryset=Facility.objects.all(),
        required=True,
        label=_("Оберіть батьківський об'єкт"),
        widget=SelectWithFormControlClass(attrs={'size': 7}),
        empty_label=None
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
        buttons = (create_primary_button(_("Додати об'єкт")),)


class FacilityEditForm(
    CrispyFormsMixin, forms.ModelForm, AdditionalSetupRequiredFormMixin
):
    # info only field, qs is filled in custom method
    descendants = SecureModelChoiceField(
        queryset=Facility.objects.none(),
        label=_("Підлеглі об'єкти"),
        empty_label=None,
        required=False,
        disabled=True,
        widget=SelectWithFormControlClass(attrs={'size': 7}),
        label_from_instance_function=common_facility_choices_format_function
    )
    # info only field, qs is filled in custom method
    roles_that_have_access_to_this_facility = SecureModelChoiceField(
        queryset=UserRole.objects.none(),
        label=_('Ролі, що мають доступ'),
        empty_label=None,
        required=False,
        disabled=True,
        widget=SelectWithFormControlClass(attrs={'size': 5}),
        label_from_instance_function=label_from_user_role_for_facility_roles
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
            'institution': forms.Textarea(attrs={'rows': 1})
        }
        buttons = UPDATE_DELETE_BUTTONS_SET

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        facility: Facility = obj
        self.fields['descendants'].queryset = facility.get_descendants()
        self.fields['roles_that_have_access_to_this_facility'].queryset = facility.users_roles
