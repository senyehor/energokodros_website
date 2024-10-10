import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

from energy.logic.run_aggregation import AGGREGATION_RUNNER, AGGREGATION_STATE_RETRIEVER
from energy.logic.run_aggregation.exceptions import RunAggregationExceptionBase

logger = logging.getLogger(__name__)


@login_required
def run_aggregation(request: HttpRequest) -> JsonResponse:
    try:
        AGGREGATION_RUNNER.run_aggregation()
    except RunAggregationExceptionBase as e:
        logger.error(e, exc_info=True)
        return JsonResponse(
            {'message': 'unexpected error happened'},
            status=400
        )
    return JsonResponse({'message': 'aggregation started successfully'})


@login_required
def get_aggregation_status_and_last_time_run(request: HttpRequest):
    _ = AGGREGATION_STATE_RETRIEVER
    return JsonResponse(
        {
            'aggregation_status':        _.get_state(),
            'aggregation_last_rime_run': _.get_last_time_aggregation_was_run(formatted=True)
        }
    )
