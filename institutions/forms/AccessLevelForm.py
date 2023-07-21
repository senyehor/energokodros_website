from django import forms
from django.utils.translation import gettext_lazy as _

from institutions.models import AccessLevel
from utils.forms import CrispyFormsMixin


class AccessLevelForm(forms.ModelForm, CrispyFormsMixin):
    class Meta:
        model = AccessLevel
        fields = ('code', 'description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__add_decision_button()

    def __add_decision_button(self):
        self.add_submit_button_at_the_end(
            _('Надіслати')
        )
