from django.urls import path

from institutions.api.views import FacilityListCreate

urlpatterns = [
    path('facilities/', FacilityListCreate.as_view())
]
