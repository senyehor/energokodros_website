from django.contrib import messages
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, ListView, UpdateView

from energokodros.settings import DEFAULT_PAGINATE_BY
from institutions.forms import FacilityEditForm, InstitutionForm
from institutions.models import Facility
from utils.common import admin_rights_required, get_object_by_hashed_id_or_404
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
class UpdateFacilityView(UpdateView):
    model = Facility
    form_class = FacilityEditForm
    template_name = 'institutions/edit_facility.html'
    success_url = reverse_lazy('facilities-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        facility = get_object_or_404(Facility, pk=self.kwargs.get('pk'))
        data['form'].fill_initial_not_populated_automatically(facility)
        return data

    def form_valid(self, form):
        messages.success(
            self.request,
            _('Установу успішно відредаговано')
        )
        return super().form_valid(form)
