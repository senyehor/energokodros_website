from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView, UpdateView

from energokodros.settings import DEFAULT_PAGINATE_BY
from institutions.forms import FacilityEditForm, InstitutionForm
from institutions.models import Facility
from utils.common import admin_rights_required
from utils.forms import EditObjectUpdateViewMixin
from utils.list_view_filtering import QuerySetFieldsIcontainsFilterPkOrderedMixin


@admin_rights_required
class FacilitiesListView(QuerySetFieldsIcontainsFilterPkOrderedMixin, ListView):
    queryset = Facility.objects.all()
    fields_order_by_before_pk = ('depth',)
    filter_fields = ('name', 'description')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'institutions/facilities_list.html'


@admin_rights_required
class CreateInstitutionView(FormView):
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


@admin_rights_required
class EditFacilityView(EditObjectUpdateViewMixin, UpdateView):
    model = Facility
    form_class = FacilityEditForm
    template_name = 'institutions/edit_facility.html'
    success_url = reverse_lazy('facilities-list')
