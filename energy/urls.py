from django.urls import path

from energy import views
from energy.models import Box, BoxSensorSet, Sensor
from utils.common import redirect_to_object_pk_in_post

urlpatterns = [
    path(
        'aggregated-consumption/',
        views.ConsumptionPageView.as_view(),
        name='aggregated-consumption'
    ),
    path(
        'get-aggregated-consumption-for-facility/',
        views.get_consumption_with_total_consumption,
        name='get-aggregated-consumption-for-facility'
    ),
    path(
        'create-box-with-sensors/',
        views.BoxWithSensorsCreateView.as_view(),
        name='create-box-with-sensors'
    ),
    path(
        'box-list',
        views.BoxListView.as_view(),
        name='box-list',
    ),
    path(
        'edit-box/<hashed_int:pk>',
        views.BoxEditDeleteView.as_view(),
        name='edit-box'
    ),
    path(
        'sensor-list',
        views.SensorListView.as_view(),
        name='sensor-list'
    ),
    path(
        'edit-sensor/<hashed_int:pk>',
        views.SensorEditDeleteView.as_view(),
        name='edit-sensor'
    ),
    path(
        'box-sensor-set-list',
        views.BoxSensorSetListView.as_view(),
        name='box-sensor-set-list'
    ),
    path(
        'edit-box-sensor-set/<hashed_int:pk>',
        views.BoxSensorSetEditDeleteView.as_view(),
        name='edit-box-sensor-set'
    )
]

ajax_url = [
    path(
        'edit-sensor-pk-in-post',
        redirect_to_object_pk_in_post(Sensor, 'edit-sensor'),
        name='edit-sensor-pk-in-post',
    ),
    path(
        'edit-box-pk-in-post',
        redirect_to_object_pk_in_post(Box, 'edit-box'),
        name='edit-box-pk-in-post'
    ),
    path(
        'edit-box-sensor-set-pk-in-post',
        redirect_to_object_pk_in_post(BoxSensorSet, 'edit-box-sensor-set'),
        name='edit-box-sensor-set-pk-in-post'
    ),
    path(
        'run-aggregation/',
        views.run_aggregation,
        name='run-aggregation'
    ),
    path(
        'get-aggregation-status-and-last-time-run/',
        views.get_aggregation_status_and_last_time_run,
        name='get-aggregation-status-and-last-time-run'
    ),
    path(
        'get-energy-report/',
        views.get_energy_report,
        name='get-energy-report'
    )
]

urlpatterns += ajax_url
