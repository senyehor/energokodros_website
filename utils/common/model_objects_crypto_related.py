from django.db.models import Manager, Model, QuerySet
from django.db.models.base import ModelBase
from django.shortcuts import get_object_or_404

from utils.forms import INT_HIDER, INT_REVEALER


def get_object_by_hashed_id_or_404(klass: ModelBase | Manager | QuerySet, hashed_id: str) -> Model:
    return get_object_or_404(klass, pk=INT_REVEALER(hashed_id))


def hash_id(model_object: Model) -> str:
    return INT_HIDER(model_object.pk)
