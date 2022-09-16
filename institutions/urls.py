from django.urls import path

from institutions.views import (
    CreateFacilityView, CreateInstitutionView, FacilitiesListView,
    get_institution_facilities_choices,
)

urlpatterns = [
    path(
        'institutions/',
        FacilitiesListView.as_view(),
        name='facilities-list'
    ),
    path(
        'new-institution/',
        CreateInstitutionView.as_view(),
        name='new-institution'
    ),
    path(
        'new-facility/',
        CreateFacilityView.as_view(),
        name='new-facility'
    ),
    path(
        'get-institution-facilities/',
        get_institution_facilities_choices,
        name='get-institution-facilities'
    )
]
