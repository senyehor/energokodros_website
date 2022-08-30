from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _

from institutions.models import Facility
from utils.forms import CrispyFormsMixin


class InstitutionForm(ModelForm, CrispyFormsMixin):
    class Meta:
        model = Facility
        fields = ('name', 'description')
        labels = {
            'name':        _('Назва'),
            'description': _('Опис')
        }
        widgets = {
            'description': Textarea(attrs={'rows': 3})
        }

    def save(self, commit=True):
        if self.errors:
            # pass raising exception to base class
            super().save()
        Facility.add_root(instance=self.instance)
        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_submit_button_at_the_end('Створити заклад')
