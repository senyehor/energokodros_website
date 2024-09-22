from rest_framework.generics import ListCreateAPIView

from institutions.api.serializers import FacilitySerializer
from institutions.models import Facility


class FacilityListCreate(ListCreateAPIView):
    serializer_class = FacilitySerializer

    def get_queryset(self):
        return Facility.objects.get_institutions()
