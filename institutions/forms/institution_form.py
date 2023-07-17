from django.db.transaction import atomic
from django.forms import Textarea
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

from institutions.logic.create_admin_roles_for_new_institution import \
    create_admin_roles_for_new_institution
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

    @method_decorator(atomic)
    def save(self, commit=True):
        if self.errors:
            # pass raising exception to base class
            super().save()
        institution = Facility.add_root(instance=self.instance)
        create_admin_roles_for_new_institution(institution)
        return self.instance
