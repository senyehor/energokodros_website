from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from energy.forms.energy_consumption_display_page_control_form import \
    EnergyConsumptionDisplayPageControlForm
from energy.logic import AggregatedEnergyConsumptionController
from institutions.models import Facility
from utils.common import get_object_by_hashed_id_or_404


class ConsumptionPageView(FormView):
    # form_class =
    template_name = 'energy/aggregated_energy_consumption.html'
    http_method_names = ('get',)

    def get_form(self, form_class=None):
        return EnergyConsumptionDisplayPageControlForm(self.request.user)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# todo add user_role - institution decorator
def get_aggregated_consumption(request: HttpRequest) -> JsonResponse:
    _ = request.POST
    # todo add custom exception type and handle
    # todo careful int conversion
    # todo create form for conversion
    institution: Facility = get_object_by_hashed_id_or_404(Facility, _['facility_id'])  # noqa
    controller = AggregatedEnergyConsumptionController(
        int(_['period_start_epoch']),  # noqa
        int(_['period_end_epoch']),  # noqa
        int(_['aggregation_interval_seconds']),  # noqa
        institution
    )
    return JsonResponse(controller.get_consumption(), safe=False)
