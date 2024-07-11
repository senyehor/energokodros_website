from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpRequest, JsonResponse

from energy.logic.aggregated_consumption import (
    AggregatedEnergyConsumptionController,
    convert_request_post_dict_to_regular_dict, EnergyConsumptionExceptionWithMessage,
)
from energy.logic.consumption_report.docx import ReportCreator
from utils.common.decoration import decorate_class_or_function_view


@decorate_class_or_function_view(login_required)
def get_energy_report(request: HttpRequest):
    try:
        # noinspection PyTypeChecker
        raw_parameters = convert_request_post_dict_to_regular_dict(request.POST)
        controller = AggregatedEnergyConsumptionController(request.user, raw_parameters)
        consumption_with_optional_forecast, total_consumption = \
            controller.get_consumption_with_optional_forecast_and_total_consumption()
    except EnergyConsumptionExceptionWithMessage as e:
        return JsonResponse(e.message, status=400, safe=False)
    report = ReportCreator(
        consumption_with_optional_forecast, total_consumption, controller.get_parameters()
    ).create_report()
    return FileResponse(report, filename='report.docx')
