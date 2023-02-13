from typing import Any, Callable

from django.db.models import Manager, Model, QuerySet
from django.db.models.base import ModelBase
from django.shortcuts import get_object_or_404

from utils.forms import INT_HIDER, INT_REVEALER, SecureModelChoiceField

Choices = list[tuple[str, str]]


def compose_secure_choices_for_queryset(
        qs: QuerySet,
        label_from_instance_function: Callable[[Any], str] = None
) -> Choices:
    choices = SecureModelChoiceField(
        queryset=qs, empty_label=None,
        label_from_instance_function=label_from_instance_function
    ).choices
    return [(str(value), label) for value, label in choices]


def get_object_by_hashed_id_or_404(_class: ModelBase | Manager | QuerySet, hashed_id: str) -> Model:
    try:
        return get_object_or_404(_class, pk=INT_REVEALER(hashed_id))
    except ValueError as e:
        raise Http404 from e


def hash_id(model_object: Model) -> str:
    return INT_HIDER(model_object.pk)
