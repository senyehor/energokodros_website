from django import forms
from django.contrib.auth import forms as auth_forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from institutions.models import Institution, AccessLevel
from users.models import User, UserRegistrationRequest


class LoginForm(auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(
        label=_("Запам'ятати мене на два тижні"),
        required=False
    )

    error_messages = {
        'invalid_login': _('Уведіть правильну електронну пошту та пароль або зареєструйтесь'),
    }


class NewUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('full_name', 'email')


class UserRegistrationRequestForm(forms.ModelForm):
    institution = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        label=_('Оберіть установу')
    )
    message = forms.CharField(
        max_length=200,
        label=_('Залиште опціональне повідомлення'),
        required=False,
        widget=forms.Textarea
    )

    class Meta:
        model = UserRegistrationRequest
        fields = ('institution', 'message')


class UserRegistrationRequestsDecisionForm(forms.Form):
    users_registration_requests = forms.ModelChoiceField(
        queryset=UserRegistrationRequest.objects.all(),
        label=_('Запити користувачів на реєстрацію')
    )
    access_level = forms.ModelChoiceField(
        queryset=AccessLevel.objects.all(),
        label=_('Призначте рівень доступу'),
        required=False
    )
    position = forms.CharField(
        max_length=100,
        widget=forms.Textarea,
        required=True,
        label=_('Уведіть позицію')
    )
    message = forms.CharField(
        max_length=255,
        widget=forms.Textarea,
        required=False,
        label=_('Залиште опціональне повідомлення для користувача')
    )


UserRegistrationRequestFormset = inlineformset_factory(
    parent_model=User,
    model=UserRegistrationRequest,
    form=UserRegistrationRequestForm,
    extra=1,
    can_delete=False,
    min_num=1,
    max_num=1
)
