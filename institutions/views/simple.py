from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from institutions.forms import FacilityEditForm, InstitutionForm
from institutions.logic import get_facilities_formatted_choices_for_user_role
from institutions.models import Facility
from users.logic import check_role_belongs_to_user
from users.models import UserRole
from utils.common import admin_rights_and_login_required, get_object_by_hashed_id_or_404
from utils.views import ListViewWithFiltering
from utils.views.edit_object_update_view import EditDeleteObjectUpdateView


@admin_rights_and_login_required
class FacilitiesListView(ListViewWithFiltering):
    queryset = Facility.objects.all()
    fields_order_by_before_pk = ('depth',)
    filter_fields = ('name', 'description')
    template_name = 'institutions/facility_list.html'


@admin_rights_and_login_required
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


@admin_rights_and_login_required
class EditFacilityView(EditDeleteObjectUpdateView):
    model = Facility
    form_class = FacilityEditForm
    template_name = 'institutions/edit_facility.html'
    success_url = reverse_lazy('facilities-list')


@login_required
def get_facilities_choices_for_role(request: HttpRequest) -> JsonResponse:
    # noinspection PyTypeChecker
    role: UserRole = get_object_by_hashed_id_or_404(
        UserRole, request.POST.get('role_id')
    )
    check_role_belongs_to_user(request.user, role)
    choices = get_facilities_formatted_choices_for_user_role(role)
    return JsonResponse(choices, safe=False)
