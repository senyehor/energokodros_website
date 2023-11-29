from django.urls import path

from institutions.models import Facility
from institutions.views import (
    CreateFacilityView, CreateInstitutionView, FacilitiesListView,
    get_institution_facilities_choices, EditFacilityView,
)
from utils.common import redirect_to_object_pk_in_post

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
        EditFacilityView.as_view(),
        name='edit-facility'
    )
]

helper_urls = [
    path(
        'edit-facility-pk-in-post/',
        redirect_to_object_pk_in_post(Facility, 'edit-facility'),
        name='edit-facility-pk-in-post'
    )
]

urlpatterns += helper_urls
