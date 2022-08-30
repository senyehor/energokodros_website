from django.urls import path

from institutions.views.simple import InstitutionCreateView, InstitutionsListView

urlpatterns = [
    path(
        'institutions/',
        InstitutionsListView.as_view(),
        name='institutions-list'
    ),
    path(
        'new-institution',
        InstitutionCreateView.as_view(),
        name='new-institution'
    )
]
