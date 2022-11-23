from django.urls import path

from institutions.views import (
    CreateFacilityView, CreateInstitutionView, FacilitiesListView,
    get_institution_facilities_choices, redirect_to_edit_facility_by_post_pk, UpdateFacilityView
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
    ),
    path(
        'edit-facility/<hashed_int:pk>',
        UpdateFacilityView.as_view(),
        name='edit-facility'
    )
]

helper_urls = [
    path(
        'edit-facility-link-pk-in-post-redirect/',
        redirect_to_edit_facility_by_post_pk,
        name='edit-facility-link-by-pk-in-post-redirect'
    )
]

urlpatterns += helper_urls
