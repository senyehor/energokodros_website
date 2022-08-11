from django.views.generic import ListView

from energokodros.settings import DEFAULT_PAGINATE_BY
from institutions.models import Facility


class InstitutionsList(ListView):
    queryset = Facility.objects.get_institutions()
    filter_fields = ('name', 'description')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'institutions'
