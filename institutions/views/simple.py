from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView

from administrator.decorators import admin_rights_required
from energokodros.settings import DEFAULT_PAGINATE_BY
from institutions.forms.institution_form import InstitutionForm
from institutions.models import Facility
from utils.filters import QuerySetFieldsIcontainsFilterPkOrderedMixin


@admin_rights_required
class FacilitiesListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    # ordering by depth to show institutions first
    queryset = Facility.objects.all().order_by('depth')
    filter_fields = ('name', 'description')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'institutions/facilities_list.html'


@admin_rights_required
class InstitutionCreateView(FormView):
    form_class = InstitutionForm
    template_name = 'institutions/new_institution.html'
    success_url = reverse_lazy('facilities-list')

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            _('Установу успішно додано')
        )
        return super().form_valid(form)
