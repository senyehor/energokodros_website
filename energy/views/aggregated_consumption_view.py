from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from energy.forms import EnergyConsumptionDisplayPageControlForm
from energy.logic import (
    AggregatedEnergyConsumptionController,
    EnergyConsumptionExceptionWithMessage,
)
from energy.logic.aggregated_consumption.simple import convert_request_post_dict_to_raw_parameters


class ConsumptionPageView(FormView):
    template_name = 'energy/consumption/aggregated_energy_consumption.html'
    http_method_names = ('get',)

    def get_form(self, form_class=None):
        return EnergyConsumptionDisplayPageControlForm(self.request.user)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def get_aggregated_consumption(request: HttpRequest) -> JsonResponse:
    try:
        # noinspection PyTypeChecker
        parameters = convert_request_post_dict_to_raw_parameters(request.POST)
        controller = AggregatedEnergyConsumptionController(request.user, parameters)
        consumption = controller.get_consumption()
    except EnergyConsumptionExceptionWithMessage as e:
        return JsonResponse(e.message, status=400, safe=False)
    return JsonResponse(consumption, safe=False)
