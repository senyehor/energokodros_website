from django.urls import path

from institutions.views.simple import FacilitiesListView, InstitutionCreateView

urlpatterns = [
    path(
        'institutions/',
        FacilitiesListView.as_view(),
        name='facilities-list'
    ),
    path(
        'new-institution/',
        InstitutionCreateView.as_view(),
        name='new-institution'
    )
]
