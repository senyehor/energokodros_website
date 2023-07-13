from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from django import forms
from django.utils.decorators import classonlymethod
from django.utils.translation import gettext_lazy as _

from institutions.models import AccessLevel, Institution
from users.models import User, UserRole, UserRoleApplication
from utils.common import generate_submit_type_button
from utils.forms import SecureModelChoiceField


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
        form_fields_order = \
            (
                'user_with_email',
                'institution_verbose',
                'message_from_user',  # info readonly fields
            ) + fields + ('message_for_user',)

    @classonlymethod
    def create_from_application_request(cls, application_request: UserRoleApplication):
        obj = cls(initial={
            'user':        application_request.user,
            'institution': application_request.institution
        })
        obj.__additionally_setup_form(application_request)
        return obj

    def __additionally_setup_form(self, application_request: UserRoleApplication):  # pylint: disable=W0238
        self.__add_readonly_prepopulated_fields(application_request)
        self.__hide_fields()
        self.__order_fields()
        self.__add_decision_buttons()
        self._errors = None

    def __hide_fields(self):
        self.helper = FormHelper(self)
        for field in self.Meta.fields_to_hide:
            self.helper[field].wrap(Div, css_class="d-none")

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

        def get_wrapped_field_name_if_div(_field: Div | str) -> str:
            if isinstance(_field, str):
                return _field
            if len(_field.fields) != 1:
                raise ValueError('only one wrapped field expected')
            return _field.fields[0]

        field_names = list(map(
            get_wrapped_field_name_if_div, unordered_fields
        ))
        ordered_fields = []
        for field in self.Meta.form_fields_order:
            ordered_fields.append(self.helper.layout.fields[field_names.index(field)])
        self.helper.layout.fields = ordered_fields

    def __add_decision_buttons(self):
        self.helper.layout.append(
            generate_submit_type_button(
                _('Підтвердити'),
                'accept'
            )
        )
        self.helper.layout.append(
            generate_submit_type_button(
                _('Відхилити'),
                'decline',
            )
        )

    @property
    def application__user(self) -> User:  # pylint: disable=R1710
        if user := self.cleaned_data.get('user', None):
            # case when validation went successfully
            return user
        # case when validation failed, but fail was suppressed,
        # as admin declined application, so no validation is actually needed
        # (required field to accept user is not needed for declining)
        if user_bound_field := self._bound_fields_cache.get('user', None):
            # VERY WEIRD when I run debug, this case works
            return user_bound_field.field.clean(self.data['user'])
        for name, bound_field in self._bound_items():
            # VERY WEIRD when I run regularly, this case works
            if name == 'user':
                return bound_field.field.clean(self.data['user'])

    @property
    def application__institution(self) -> Institution:
        # we need access to institution only when accepting,
        # so there is no need to do it similarly to application__user property
        return self.cleaned_data['institution']

    def get_message_for_user(self) -> str:
        return self.data['message_for_user']
