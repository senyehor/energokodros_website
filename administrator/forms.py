from django import forms
from django.utils.translation import gettext_lazy as _

from institutions.models import AccessLevel
from users.models import UserRegistrationRequest


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
