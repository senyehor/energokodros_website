from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from energy.forms import (
    BoxForm, BoxSensorSetForBoxWithSensorsCreationForm,
    SensorForm,
)
from energy.logic.ajax import get_facilities_formatted_choices_for_user_role
from energy.models import Box, BoxSensorSet, Sensor
from users.logic.simple import check_role_belongs_to_user
from users.models import UserRole
from utils.common import admin_rights_and_login_required, get_object_by_hashed_id_or_404
from utils.views import EditDeleteObjectUpdateView, ListViewWithFiltering


@admin_rights_and_login_required
class BoxListView(ListViewWithFiltering):
    queryset = Box.objects.all()
    filter_fields = ('identifier', 'description')
    template_name = 'energy/box_list.html'


@admin_rights_and_login_required
class BoxEditDeleteView(EditDeleteObjectUpdateView):
    model = Box
    form_class = BoxForm
    success_url = reverse_lazy('box-list')
    template_name = 'energy/edit_box.html'
    EDIT_SUCCESS_MESSAGE = _('Ящик успішно відредаговано')


@admin_rights_and_login_required
class SensorListView(ListViewWithFiltering):
    queryset = Sensor.objects.all()
    filter_fields = ('sensor_number', 'sensor_description')
    template_name = 'energy/sensor_list.html'


@admin_rights_and_login_required
class SensorEditDeleteView(EditDeleteObjectUpdateView):
    model = Sensor
    form_class = SensorForm
    success_url = reverse_lazy('sensor-list')
    template_name = 'energy/edit_sensor.html'
    EDIT_SUCCESS_MESSAGE = _('Сенсор успішно відредаговано')


@admin_rights_and_login_required
class BoxSensorSetListView(ListViewWithFiltering):
    queryset = BoxSensorSet.objects.all()
    filter_fields = ('facility__name', 'line_name', 'box__identifier')
    template_name = 'energy/box_sensor_set_list.html'


@admin_rights_and_login_required
class BoxSensorSetEditDeleteView(EditDeleteObjectUpdateView):
    model = BoxSensorSet
    form_class = BoxSensorSetForm
    success_url = reverse_lazy('box-sensor-set-list')
    template_name = 'energy/edit_box_sensor_set.html'
    EDIT_SUCCESS_MESSAGE = _('Набір успішно відредаговано')


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
