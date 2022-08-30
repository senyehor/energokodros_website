from django.views.generic import FormView, ListView

from energokodros.settings import DEFAULT_PAGINATE_BY
from institutions.forms.institution_form import InstitutionForm
from institutions.models import Facility


class InstitutionsListView(ListView):
    queryset = Facility.objects.get_institutions()
    filter_fields = ('name', 'description')
    paginate_by = DEFAULT_PAGINATE_BY
    template_name = 'institutions/institutions_list.html'


class InstitutionCreateView(FormView):
    form_class = InstitutionForm
    template_name = 'institutions/new_institution.html'
