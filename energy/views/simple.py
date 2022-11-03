from django.http import HttpRequest, JsonResponse

from energy.logic.ajax import get_facilities_formatted_choices_for_user_role
from users.logic.simple import check_role_belongs_to_user
from users.models import UserRole
from utils.common import get_object_by_hashed_id_or_404


def get_facilities_choices_for_role(request: HttpRequest) -> JsonResponse:
    # noinspection PyTypeChecker
    role: UserRole = get_object_by_hashed_id_or_404(
        UserRole,
        request.POST.get('role_id')
    )
    check_role_belongs_to_user(request.user, role)
    choices = get_facilities_formatted_choices_for_user_role(
        role
    )
    return JsonResponse(choices, safe=False)