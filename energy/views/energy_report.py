from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpRequest, JsonResponse

from energy.logic.aggregated_consumption import (
    ConsumptionWithOptionalForecastQuerierFromRawParameter,
    convert_request_post_dict_to_regular_dict, EnergyConsumptionExceptionWithMessage,
)
from energy.logic.consumption_report.docx import ReportCreator
from utils.common.decoration import decorate_class_or_function_view


@decorate_class_or_function_view(login_required)
def get_energy_report(request: HttpRequest):
    # noinspection PyTypeChecker
    raw_parameters = convert_request_post_dict_to_regular_dict(request.POST)
    try:
        querier = ConsumptionWithOptionalForecastQuerierFromRawParameter(
            request.user, raw_parameters
        )
        raw_and_formatted_consumption_with_raw_and_formatted_optional_forecast = \
            querier.get_raw_and_formatted_consumption_with_raw_and_formatted_optional_forecast()
        total_consumption = querier.get_total_consumption()
    except EnergyConsumptionExceptionWithMessage as e:
        return JsonResponse(e.message, status=400, safe=False)
    if not raw_and_formatted_consumption_with_raw_and_formatted_optional_forecast:
        # todo fix via uniform response with metadata
        return FileResponse(None)
    report = ReportCreator(
        raw_and_formatted_consumption_with_raw_and_formatted_optional_forecast,
        total_consumption,
        querier.get_parameters()
    ).create_report()
    return FileResponse(report, filename='report.docx')
