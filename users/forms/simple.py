from django import forms
from django.contrib.auth import forms as auth_forms
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from institutions.models import Facility
from users.logic.simple import format_user_role
from users.models import User, UserRole, UserRoleApplication
from utils.common import object_to_queryset
from utils.forms import (
    create_primary_button, CrispyFormsMixin, SecureModelChoiceField,
    SelectWithFormControlClass, UPDATE_DELETE_BUTTONS_SET,
)


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


class UserRoleApplicationForm(CrispyFormsMixin, forms.ModelForm):
    institution = SecureModelChoiceField(
        label=_('Оберіть заклад'),
        queryset=Facility.objects.get_institutions(),
        widget=SelectWithFormControlClass({'size': 4}),
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
        buttons = (create_primary_button(_('Відправити заявку на реєстрацію')),)

    def set_user(self, user: User):
        """be careful, no user validation is run here"""
        self.instance.user = user


class EditUserForm(CrispyFormsMixin, forms.ModelForm):
    # info only field, qs is filled in custom method
    roles = SecureModelChoiceField(
        queryset=UserRole.objects.none(),
        label=_("Ролі"),
        empty_label=None,
        required=False,
        disabled=True,
        widget=SelectWithFormControlClass(attrs={'size': 4}),
        label_from_instance_function=format_user_role
    )
    full_name = forms.CharField(
        label=_("Повне ім'я"),
        required=False,
        disabled=True,
    )
    email = forms.CharField(
        label=_('Електронна пошта'),
        required=False,
        disabled=True,
    )

    class Meta:
        model = User
        fields = ('full_name', 'email', 'is_admin')
        buttons = UPDATE_DELETE_BUTTONS_SET

    def additionally_fill(self, operated_object: Model):
        # noinspection PyTypeChecker
        user: User = operated_object
        self.fields['roles'].queryset = user.roles


class EditUserRole(CrispyFormsMixin, forms.ModelForm):
    # should be prepopulated in corresponding method
    user_info = SecureModelChoiceField(
        queryset=User.objects.none(),
        label=_("Користувач"),
        required=False,
        disabled=True,
        empty_label=None,
        widget=SelectWithFormControlClass(attrs={'size': 1}),
    )
    # should be prepopulated in corresponding method
    facility_has_access_to_info = SecureModelChoiceField(
        queryset=Facility.objects.none(),
        label=_("Об'єкт"),
        required=False,
        disabled=True,
        empty_label=None,
        widget=SelectWithFormControlClass(attrs={'size': 1}),
    )

    class Meta:
        model = UserRole
        fields = ('position_name',)
        buttons = UPDATE_DELETE_BUTTONS_SET

    def additionally_fill(self, operated_object: Model):
        # noinspection PyTypeChecker
        role: UserRole = operated_object
        self.fields['user_info'].queryset = object_to_queryset(role.user)
        self.fields['facility_has_access_to_info'].queryset = \
            object_to_queryset(role.facility_has_access_to)
