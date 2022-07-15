from django import forms
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _

from institutions.models import AccessLevel, Institution
from users.models import User, UserRole, UserRoleApplication
from utils.forms import CrispyFormsMixin, SecureModelChoiceField


class UserRoleApplicationRequestsDecisionForm(forms.ModelForm, CrispyFormsMixin):
    """This form must be created from a user role application"""
    access_level = SecureModelChoiceField(
        label=_('Призначте рівень доступу'),
        queryset=AccessLevel.objects.all(),
        required=True
    )
    position = forms.CharField(
        label=_('Призначте позицію'),
        max_length=255,
        required=True,
    )
    message_for_user = forms.CharField(
        label=_('Залиште опціональне повідомлення для користувача'),
        max_length=255,
        required=False,
        widget=forms.Textarea({'rows': 2})
    )
    user = SecureModelChoiceField(
        queryset=User.objects.all(),
    )
    institution = SecureModelChoiceField(
        queryset=Institution.objects.all(),
    )

    class Meta:
        model = UserRole
        # user and institution is added in custom creation method
        fields_to_hide = ('user', 'institution')
        fields = ('access_level', 'position') + fields_to_hide
        info_readonly_fields = (
            'user_with_email',
            'institution_verbose',
            'message_from_user',
        )
        fields_order = info_readonly_fields + fields + ('message_for_user',)

    @classonlymethod
    def create_from_role_application(cls, application_request: UserRoleApplication):
        obj = cls(initial={
            'user':        application_request.user,
            'institution': application_request.institution
        })
        obj.__additionally_setup_form(application_request)
        return obj

    def __additionally_setup_form(self, application_request: UserRoleApplication):  # pylint: disable=W0238
        self.__add_readonly_prepopulated_fields(application_request)
        self.__order_fields()
        self.__add_decision_buttons()
        self.hide_fields()
        self._errors = None

    def __add_readonly_prepopulated_fields(self, application_request: UserRoleApplication):
        # this fields will not be used in UserRole creation, so required = False
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

    def __order_fields(self):
        unordered_fields = self.helper.layout.fields
        # using map to 'reveal' field names if they are wrapped in a div
        field_names = list(map(
            self._get_wrapped_field_name_if_div, unordered_fields
        ))
        ordered_fields = []
        for field in self.Meta.fields_order:
            ordered_fields.append(self.helper.layout.fields[field_names.index(field)])
        self.helper.layout.fields = ordered_fields

    def __add_decision_buttons(self):
        self.add_button_at_the_end(
            _('Підтвердити'),
            'accept'
        )
        self.add_button_at_the_end(
            _('Відхилити'),
            'decline',
        )

    def get_message_for_user(self) -> str:
        return self.data['message_for_user']
