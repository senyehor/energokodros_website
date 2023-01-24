from django.urls import path

from energy import views

urlpatterns = [
    path(
        'aggregated-consumption/',
        views.ConsumptionPageView.as_view(),
        name='aggregated-consumption'
    ),
    path(
        'get-facilities-list-for-role/',
        views.get_facilities_choices_for_role,
        name='get-facilities-list-for-role'
    ),
    path(
        'get-aggregated-consumption-for-facility/',
        views.get_aggregated_consumption,
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
