from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.generic import FormView

from energy.forms import EnergyConsumptionDisplayPageControlForm
from energy.logic import (
    AggregatedEnergyConsumptionController,
    EnergyConsumptionExceptionWithMessage,
)
from energy.logic.aggregated_consumption import show_no_roles_page_if_user_has_no_roles
from energy.logic.aggregated_consumption.simple import convert_request_post_dict_to_raw_parameters
from utils.common.decoration import decorate_class_or_function_view


@decorate_class_or_function_view(login_required)
@decorate_class_or_function_view(show_no_roles_page_if_user_has_no_roles)
class ConsumptionPageView(FormView):
    template_name = 'energy/consumption/aggregated_energy_consumption.html'

    def get_form(self, form_class=None):
        return EnergyConsumptionDisplayPageControlForm(self.request.user)


def get_aggregated_consumption(request: HttpRequest) -> JsonResponse:
    try:
        # noinspection PyTypeChecker
        parameters = convert_request_post_dict_to_raw_parameters(request.POST)
        controller = AggregatedEnergyConsumptionController(request.user, parameters)
        consumption = controller.get_consumption()
    except EnergyConsumptionExceptionWithMessage as e:
        return JsonResponse(e.message, status=400, safe=False)
    return JsonResponse(consumption, safe=False)
