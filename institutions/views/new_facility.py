from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from administrator.decorators import admin_rights_required
from institutions.forms import NewFacilityForm
from institutions.logic import (
    compose_formatted_institution_facilities_choices,
    get_institution_by_hashed_id,
)
from institutions.models import Facility


@admin_rights_required
def get_institution_facilities_choices(request) -> JsonResponse:
    hashed_institution_id = request.POST.get('institution_id')
    institution = get_institution_by_hashed_id(hashed_institution_id)
    formatted_choices_ordered = compose_formatted_institution_facilities_choices(institution)
    return JsonResponse(formatted_choices_ordered, safe=False)


@admin_rights_required
class CreateFacilityView(FormView):
    template_name = 'institutions/new_facility.html'
    form_class = NewFacilityForm
    success_url = reverse_lazy('facilities-list')

    def form_valid(self, form):
        parent_facility: Facility = form.cleaned_data['parent_facility']
        new_facility = form.save(commit=False)
        parent_facility.add_child(instance=new_facility)
        messages.success(self.request, _("Об'єкт успішно додано"))
        return super().form_valid(form)
