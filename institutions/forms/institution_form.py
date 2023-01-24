from django.forms import Textarea
from django.utils.translation import gettext_lazy as _

from institutions.models import Facility
from utils.forms import create_primary_button, CrispyModelForm


class InstitutionForm(CrispyModelForm):
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
        buttons = (create_primary_button(_('Додати установу')),)

    def save(self, commit=True):
        if self.errors:
            # pass raising exception to base class
            super().save()
        Facility.add_root(instance=self.instance)
        return self.instance
