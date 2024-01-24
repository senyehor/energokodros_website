from django import forms
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _

from institutions.logic import common_facility_choices_format_function
from institutions.models import Facility
from users.models import UserRole, UserRoleApplication
from utils.forms import (
    create_danger_button, create_primary_button, CrispyModelForm,
    SecureModelChoiceField,
    SelectWithFormControlClass,
)


class UserRoleApplicationRequestsDecisionForm(CrispyModelForm):
    """This form must be created from a user role application"""
    # qs set to all to allow any facility to be chosen
    # correct qs for institution is set in custom creating method
    facility_has_access_to = SecureModelChoiceField(
        label=_("Оберіть об'єкт до якого користувач матиме доступ"),
        queryset=Facility.objects.all(),
        required=True,
        empty_label=None,
        label_from_instance_function=common_facility_choices_format_function,
        widget=SelectWithFormControlClass({'size': 6})
    )
    position_name = forms.CharField(
        label=_('Уведіть назву позиції'),
        max_length=255,
        required=True,
    )
    message_for_user = forms.CharField(
        label=_('Залиште опціональне повідомлення для користувача'),
        max_length=255,
        required=False,
        widget=forms.Textarea({'rows': 2})
    )
    # info readonly fields
    user_with_email = forms.CharField(
        label=_('Користувач та пошта'),
        max_length=255,
        widget=forms.TextInput({'readonly': 'readonly'}),
        required=False
    )
    institution_verbose = forms.CharField(
        label=_('Установа'),
        max_length=255,
        widget=forms.TextInput({'readonly': 'readonly'}),
        required=False
    )
    message_from_user = forms.CharField(
        label=_('Повідомлення від користувача'),
        max_length=255,
        widget=forms.Textarea({'rows': 2, 'readonly': 'readonly'}),
        required=False
    )

    class Meta:
        model = UserRole
        fields = ('position_name', 'facility_has_access_to')
        info_readonly_fields = (
            'user_with_email',
            'institution_verbose',
            'message_from_user',
        )
        fields_order = info_readonly_fields + fields + ('message_for_user',)
        buttons = (
            create_primary_button(
                _('Підтвердити'),
                name='decision',
                value='accept'
            ),
            create_danger_button(
                _('Відхилити'),
                name='decision',
                value='decline'
            )
        )

    @classonlymethod
    def create_from_role_application(cls, application_request: UserRoleApplication):
        obj = cls()
        obj.__additionally_setup_form(application_request)
        return obj

    # pylint bug so have to be disabled pylint: disable-next=W0238
    def __additionally_setup_form(self, application_request: UserRoleApplication):
        self.__set_correct_queryset_for_facility_has_access_to(application_request.institution)
        self.__populate_info_fields(application_request)

    def __set_correct_queryset_for_facility_has_access_to(self, institution: Facility):
        self.fields['facility_has_access_to'].queryset = \
            Facility.objects.get_all_institution_objects(institution)

    def __populate_info_fields(self, application_request: UserRoleApplication):
        self.fields['institution_verbose'].initial = _(str(application_request.institution))
        self.fields['user_with_email'].initial = \
            _(f'{application_request.user} {application_request.user.email}')
        self.fields['message_from_user'].initial = _(application_request.message)

    def get_message_for_user(self) -> str:
        return self.data['message_for_user']
