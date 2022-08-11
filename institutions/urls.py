from django.urls import path

from institutions.views.simple import InstitutionsList

urlpatterns = [
    path(
        'institutions-and-objects/',
        InstitutionsList.as_view(),
        name='institutions-and-objects'
    ),
]
