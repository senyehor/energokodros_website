from django import forms
from django.contrib.auth import forms as auth_forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from institutions.models import Institution
from users.models import User, UserRoleApplication
from utils.forms import SecureModelChoiceField


class LoginForm(auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(
        label=_("Запам'ятати мене на два тижні"),
        required=False
    )

    error_messages = {
        'invalid_login': _('Уведіть правильну електронну пошту та пароль або зареєструйтесь'),
        'inactive':      _('Електронна пошта ще не підтверджена'),
    }


class NewUserForm(auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('full_name', 'email')


class UserRoleApplicationForm(forms.ModelForm):
    institution = SecureModelChoiceField(
        label=_('Оберіть установу'),
        queryset=Institution.objects.all(),
    )
    message = forms.CharField(
        label=_('Залиште опціональне повідомлення'),
        max_length=200,
        required=False,
        widget=forms.Textarea({'rows': 2})
    )

    class Meta:
        model = UserRoleApplication
        fields = ('institution', 'message')


RegistrationFormset = inlineformset_factory(
    parent_model=User,
    model=UserRoleApplication,
    form=UserRoleApplicationForm,
    extra=1,
    can_delete=False,
    min_num=1,
    max_num=1
)
