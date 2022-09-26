from django import forms
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _

from institutions.models import Facility
from users.models import User, UserRoleApplication
from utils.forms import CrispyFormsMixin, SecureModelChoiceField


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


class UserRoleApplicationForm(forms.ModelForm, CrispyFormsMixin):
    institution = SecureModelChoiceField(
        label=_('Оберіть заклад'),
        queryset=Facility.objects.get_institutions(),
        required=True
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_submit_button_at_the_end(
            _('Відправити заявку на реєстрацію')
        )

    def set_valid_user(self, user: User):
        """be careful, no user validation is run here"""
        self.instance.user = user
