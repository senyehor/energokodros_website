import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

from energy.logic import get_facilities_formatted_choices_for_user_role
from energy.logic.run_aggregation import AGGREGATION_RUNNER
from energy.logic.run_aggregation.exceptions import RunAggregationExceptionBase
from users.logic.simple import check_role_belongs_to_user
from users.models import UserRole
from utils.common import get_object_by_hashed_id_or_404

logger = logging.getLogger(__name__)


@login_required
def get_facilities_choices_for_role(request: HttpRequest) -> JsonResponse:
    # noinspection PyTypeChecker
    role: UserRole = get_object_by_hashed_id_or_404(
        UserRole, request.POST.get('role_id')
    )
    check_role_belongs_to_user(request.user, role)
    choices = get_facilities_formatted_choices_for_user_role(role)
    return JsonResponse(choices, safe=False)


@login_required
def run_aggregation(request: HttpRequest) -> JsonResponse:
    try:
        AGGREGATION_RUNNER.run_aggregation()
    except RunAggregationExceptionBase as e:
        logger.error(e)
        return JsonResponse(
            'unexpected error happened',
            status=400
        )
    return JsonResponse('aggregation started successfully')
