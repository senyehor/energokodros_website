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
    )
]