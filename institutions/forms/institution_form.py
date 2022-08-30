from django.forms import ModelForm

from institutions.models import Facility
from utils.forms import CrispyFormsMixin


class InstitutionForm(ModelForm, CrispyFormsMixin):
    class Meta:
        model = Facility
        fields = ('name', 'description')

    def save(self):  # noqa pylint: disable=W0221
        if self.errors:
            # pass raising exception to base class
            super().save()
        Facility.add_root(instance=self.instance)
        return self.instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_submit_button_at_the_end('Створити заклад')