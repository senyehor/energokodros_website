from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from institutions.forms import NewFacilityForm
from institutions.logic import (
    make_institution_facilities_choices_with_padding_according_to_nesting,
)
from institutions.models import Facility
from utils.common import get_object_by_hashed_id_or_404
from utils.common.admin_rights import admin_rights_and_login_required


@admin_rights_and_login_required
def get_institution_facilities_choices(request) -> JsonResponse:
    institution: Facility = get_object_by_hashed_id_or_404(  # noqa
        Facility,
        request.POST.get('institution_id')
    )
    formatted_choices_ordered = \
        make_institution_facilities_choices_with_padding_according_to_nesting(
            institution
        )
    return JsonResponse(formatted_choices_ordered, safe=False)


@admin_rights_and_login_required
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
