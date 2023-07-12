from django import forms
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _

from institutions.models import AccessLevel, Institution
from users.models import User, UserRole, UserRoleApplication
from utils.forms import create_queryset_from_object, SecureModelChoiceField


class UserRoleApplicationRequestsDecisionForm(forms.ModelForm):
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

    class Meta:
        model = UserRole
        # user and institution is added in custom creation method
        fields = ('access_level', 'position')
        form_fields_order = (
            'user_with_email',
            'institution_verbose',
            'message_from_user',
            'access_level',
            'position',
            'message_for_user'
        )

    @classonlymethod
    def create_from_application_request(cls, application_request: UserRoleApplication):
        obj = cls()
        obj.__prepopulate_fields(application_request)
        obj.__alter_field_due_to_custom_creating()
        return obj

    def __alter_field_due_to_custom_creating(self):  # pylint: disable=W0238
        self._errors = None

    def __prepopulate_fields(self, application_request: UserRoleApplication):  # pylint: disable=W0238
        self.__add_hidden_fields(application_request)
        self.__add_visible_fields(application_request)
        self.__order_fields()

    def __add_hidden_fields(self, application_request: UserRoleApplication):
        # SecureModelChoiceField is used to hide id`s, information for users
        # should be added in __add_visible_fields
        # ModelChoiceField requires to always provide a queryset,
        # so queryset from initial object is created
        self.fields['user'] = SecureModelChoiceField(
            initial=application_request.user,
            queryset=create_queryset_from_object(application_request.user),
            widget=forms.HiddenInput()
        )
        self.fields['institution'] = SecureModelChoiceField(
            initial=application_request.institution,
            queryset=create_queryset_from_object(application_request.institution),
            widget=forms.HiddenInput()
        )

    def __add_visible_fields(self, application_request: UserRoleApplication):
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
        unordered_fields = self.fields
        ordered_fields = {field: unordered_fields[field] for field in self.Meta.form_fields_order}
        # adding fields that are not included in ordered_fields
        ordered_fields.update(unordered_fields)
        self.fields = ordered_fields

    @property
    def application_user(self) -> User:
        return self.fields['user']

    @property
    def application_institution(self) -> Institution:
        return self.fields['institution']
