from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.generic import FormView

from energy.forms import EnergyConsumptionDisplayPageControlForm
from energy.logic.aggregated_consumption import (
    AggregatedEnergyConsumptionController, convert_request_post_dict_to_regular_dict,
    EnergyConsumptionExceptionWithMessage, show_no_roles_page_if_user_has_no_roles,
)
from utils.common.decoration import decorate_class_or_function_view


@decorate_class_or_function_view(login_required)
@decorate_class_or_function_view(show_no_roles_page_if_user_has_no_roles)
class ConsumptionPageView(FormView):
    template_name = 'energy/consumption/main_page.html'

    def get_form(self, form_class=None):
        return EnergyConsumptionDisplayPageControlForm(self.request.user)


def get_consumption_with_total_consumption(request: HttpRequest) -> JsonResponse:
    try:
        # noinspection PyTypeChecker
        parameters = convert_request_post_dict_to_regular_dict(request.POST)
        controller = AggregatedEnergyConsumptionController(request.user, parameters)
        consumption, total_consumption = \
            controller.get_consumption_with_optional_forecast_and_total_consumption()
    except EnergyConsumptionExceptionWithMessage as e:
        return JsonResponse(e.message, status=400, safe=False)
    return JsonResponse(
        {'consumption': consumption, 'total_consumption': total_consumption}, safe=False
    )
