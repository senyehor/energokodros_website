from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from energy.forms import EditBoxForm
from energy.logic.ajax import get_facilities_formatted_choices_for_user_role
from energy.models import Box
from users.logic.simple import check_role_belongs_to_user
from users.models import UserRole
from utils.common import admin_rights_and_login_required, get_object_by_hashed_id_or_404
from utils.views import EditDeleteObjectUpdateView, ListViewWithFiltering


@admin_rights_and_login_required
class BoxListView(ListViewWithFiltering):
    queryset = Box.objects.all()
    filter_fields = ('box_identifier', 'box_description')
    template_name = 'energy/box_list.html'


@admin_rights_and_login_required
class BoxEditDeleteView(EditDeleteObjectUpdateView):
    model = Box
    form_class = EditBoxForm
    success_url = reverse_lazy('box-list')
    template_name = 'users/edit_user_role.html'
    EDIT_SUCCESS_MESSAGE = _('Ящик успішно відредаговано')


@login_required
def get_facilities_choices_for_role(request: HttpRequest) -> JsonResponse:
    # noinspection PyTypeChecker
    role: UserRole = get_object_by_hashed_id_or_404(
        UserRole,
        request.POST.get('role_id')
    )
    check_role_belongs_to_user(request.user, role)
    choices = get_facilities_formatted_choices_for_user_role(role)
    return JsonResponse(choices, safe=False)
