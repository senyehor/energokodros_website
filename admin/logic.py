from django.shortcuts import get_object_or_404

from admin.models import UserRegistrationRequest


def _get_message_for_registration_request(request_id: int):
    return get_object_or_404(UserRegistrationRequest, id=request_id).message
