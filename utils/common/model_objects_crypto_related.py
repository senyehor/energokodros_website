from typing import TypeAlias

from django.db.models import Manager, Model, QuerySet
from django.db.models.base import ModelBase
from django.forms import ChoiceField
from django.shortcuts import get_object_or_404

from utils.forms import INT_HIDER, INT_REVEALER, SecureModelChoiceField

Choices: TypeAlias = list[tuple[str, str]]


def compose_choices_for_queryset(
        qs: QuerySet,
        choice_field_class: type(ChoiceField) = SecureModelChoiceField) -> Choices:
    choices = choice_field_class(queryset=qs, empty_label=None).choices
    return [(str(value), label) for value, label in choices]


def get_object_by_hashed_id_or_404(klass: ModelBase | Manager | QuerySet, hashed_id: str) -> Model:
    return get_object_or_404(klass, pk=INT_REVEALER(hashed_id))


def hash_id(model_object: Model) -> str:
    return INT_HIDER(model_object.pk)
