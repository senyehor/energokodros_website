from django import forms
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _

from institutions.logic.facility_formatting_and_ajax_related import \
    SecureModelChoiceFieldWithVerboseFacilityLabeling
from institutions.models import Facility
from users.models import User, UserRole, UserRoleApplication
from utils.forms import CrispyFormsMixin, SecureModelChoiceField


class UserRoleApplicationRequestsDecisionForm(forms.ModelForm, CrispyFormsMixin):
    """This form must be created from a user role application"""
    # facility_has_access_to and user are prepopulated in create_from_role_application method but
    # set here to corresponding fields to be correctly converted to python object on submission
    facility_has_access_to = SecureModelChoiceFieldWithVerboseFacilityLabeling(
        label=_("Оберіть об'єкт до якого користувач матиме доступ"),
        queryset=Facility.objects.all(),
        required=True,
        empty_label=None
    )
    user = SecureModelChoiceField(
        queryset=User.objects.all(),
    )
    position = forms.CharField(
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

    class Meta:
        model = UserRole
        # user is added in custom creation method
        fields_to_hide = ('user',)
        fields = ('position', 'facility_has_access_to') + fields_to_hide
        info_readonly_fields = (
            'user_with_email',
            'institution_verbose',
            'message_from_user',
        )
        fields_order = info_readonly_fields + fields + ('message_for_user',)

    @classonlymethod
    def create_from_role_application(cls, application_request: UserRoleApplication):
        obj = cls(
            initial={
                'user': application_request.user,
            }
        )
        obj.__additionally_setup_form(application_request)
        return obj

    # pylint bug so have to be disabled pylint: disable-next=W0238
    def __additionally_setup_form(self, application_request: UserRoleApplication):
        self.__add_object_has_access_to_field(application_request.institution)
        self.__add_readonly_prepopulated_fields(application_request)
        self.order_fields(self.Meta.fields_order)
        self.__add_decision_buttons()
        self.hide_fields()

    def __add_object_has_access_to_field(self, institution: Facility):
        self.fields['facility_has_access_to'].queryset = \
            Facility.objects.get_all_institution_objects(institution)

    def __add_readonly_prepopulated_fields(self, application_request: UserRoleApplication):
        # these fields will not be used in UserRole creation, so required = False
        self.fields['user_with_email'] = forms.CharField(
            label=_('Користувач та пошта'),
            max_length=255,
            initial=_(f'{application_request.user} {application_request.user.email}'),
            widget=forms.TextInput({'readonly': 'readonly'}),
            required=False
        )
        self.fields['institution_verbose'] = forms.CharField(
            label=_('Установа'),
            max_length=255,
            initial=_(str(application_request.institution)),
            widget=forms.TextInput({'readonly': 'readonly'}),
            required=False
        )
        self.fields['message_from_user'] = forms.CharField(
            label=_('Повідомлення від користувача'),
            max_length=255,
            initial=_(application_request.message),
            widget=forms.Textarea({'rows': 2, 'readonly': 'readonly'}),
            required=False
        )

    def __add_decision_buttons(self):
        button_name = 'decision'
        self.add_submit_button_at_the_end(
            _('Підтвердити'),
            'accept',
            button_name
        )
        self.add_submit_button_at_the_end(
            _('Відхилити'),
            'decline',
            button_name
        )

    def get_message_for_user(self) -> str:
        return self.data['message_for_user']
