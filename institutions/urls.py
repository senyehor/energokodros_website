from django.urls import path

from institutions.views.simple import CreateInstitutionView, FacilitiesListView

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
]
