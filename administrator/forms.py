from django import forms
from django.utils.translation import gettext_lazy as _

from institutions.models import AccessLevel
from users.models import UserRoleApplication
from utils.forms import SecureModelChoiceField


class UserRegistrationRequestsDecisionForm(forms.Form):
    users_role_applications = SecureModelChoiceField(
        queryset=UserRoleApplication.objects.all(),
        label=_('Запити користувачів на реєстрацію')
    )
    access_level = SecureModelChoiceField(
        queryset=AccessLevel.objects.all(),
        label=_('Призначте рівень доступу'),
        required=False
    )
    position = forms.CharField(
        max_length=100,
        widget=forms.Textarea({'rows': 1}),
        required=True,
        label=_('Уведіть позицію')
    )
    message = forms.CharField(
        max_length=255,
        widget=forms.Textarea({'rows': 4}),
        required=False,
        label=_('Залиште опціональне повідомлення для користувача')
    )
