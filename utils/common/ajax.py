from typing import Callable, Type

from django.db.models import Model
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy

from utils.common import get_object_by_hashed_id_or_404


def redirect_to_object_pk_in_post(_class: Type[Model], redirect_to_url: str) -> Callable:
    def create_link(request: HttpRequest) -> JsonResponse:
        nonlocal _class
        nonlocal redirect_to_url
        obj = get_object_by_hashed_id_or_404(_class, request.POST.get('id'))
        return JsonResponse(
            {'url': reverse_lazy(redirect_to_url, kwargs={'pk': obj.pk})}
        )

    return create_link
