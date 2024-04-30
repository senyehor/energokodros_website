from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from energy.forms import BoxForm, BoxSensorSetForm, SensorForm
from energy.models import Box, BoxSensorSet, Sensor
from utils.common import admin_rights_and_login_required
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
