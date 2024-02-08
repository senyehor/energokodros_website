from django import forms
from django.contrib.auth import forms as auth_forms
from django.db.models import Model
from django.forms import Form
from django.utils.translation import gettext_lazy as _

from institutions.models import Facility
from users.models import User, UserRole, UserRoleApplication
from utils.common.object_to_queryset import object_to_queryset
from utils.forms import (
    create_primary_button, CrispyFormMixin, CrispyModelForm, SecureModelChoiceField,
    SelectWithFormControlClass, UPDATE_DELETE_BUTTONS_SET,
)
from utils.views import AdditionalSetupRequiredFormMixin


class LoginForm(CrispyFormMixin, auth_forms.AuthenticationForm):
    remember_me = forms.BooleanField(
        label=_("Запам'ятати мене на два тижні"),
        required=False
    )

    error_messages = {
        'invalid_login': _('Уведіть правильну електронну пошту та пароль або зареєструйтесь'),
        'inactive':      _('Електронна пошта ще не підтверджена'),
    }

    class Meta:
        buttons = (create_primary_button(_('Увійти')),)


class NewUserForm(CrispyFormMixin, auth_forms.UserCreationForm):
    class Meta:
        model = User
        fields = ('full_name', 'email')


class UserRoleApplicationForm(CrispyModelForm):
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
        buttons = (create_primary_button(_('Відправити заявку на роль')),)

    def set_application_request_user(self, user: User):
        self.instance.user = user


class UserRoleApplicationFormForRegistration(UserRoleApplicationForm):
    class Meta(UserRoleApplicationForm.Meta):
        # buttons are set here to be displayed at the bottom of registration form
        buttons = (create_primary_button(_('Відправити заявку на реєстрацію')),)


class UserForm(CrispyModelForm, AdditionalSetupRequiredFormMixin):
    # info only field, qs is filled in custom method
    roles = SecureModelChoiceField(
        queryset=UserRole.objects.none(),
        label=_("Ролі"),
        empty_label=None,
        required=False,
        disabled=True,
        widget=SelectWithFormControlClass(attrs={'size': 4}),
        label_from_instance_function=lambda user_role:
        _(f"{user_role.position_name}, об'єкт {user_role.facility_has_access_to.name}")
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

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        user: User = obj
        self.fields['roles'].queryset = user.roles


class UserRoleForm(CrispyModelForm, AdditionalSetupRequiredFormMixin):
    user_info = SecureModelChoiceField(
        queryset=User.objects.none(),
        label=_("Користувач"),
        disabled=True,
        empty_label=None
    )
    facility_has_access_to_info = SecureModelChoiceField(
        queryset=Facility.objects.none(),
        label=_("Об'єкт"),
        disabled=True,
        empty_label=None,
    )

    class Meta:
        model = UserRole
        fields = ('position_name',)
        buttons = UPDATE_DELETE_BUTTONS_SET

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        role: UserRole = obj
        self.fields['user_info'].queryset = object_to_queryset(role.user)
        self.fields['facility_has_access_to_info'].queryset = \
            object_to_queryset(role.facility_has_access_to)


class ProfileForm(Form):
    # must be set dynamically for user
    roles = SecureModelChoiceField(
        label=_('Мої ролі'),
        queryset=UserRole.objects.none(),
        widget=SelectWithFormControlClass({'size': 6}),
        empty_label=None
    )

    def __init__(self, *args, user: User, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_roles_for_user(user)

    def __set_roles_for_user(self, user: User):
        self.fields['roles'].queryset = user.roles.all()
