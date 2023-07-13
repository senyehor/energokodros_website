from typing import Literal

from django.db import models as db_models
from django.db.models import Model, QuerySet
from django.forms import models

from utils.crypto import hide_int, reveal_int


class IncorrectSecureModelFieldValue(Exception):
    pass


class SecureModelChoiceField(models.ModelChoiceField):

    def prepare_value(self, value: db_models.Model | None | Literal['']) -> str:
        if not value:
            return super().to_python(value)
        try:
            return hide_int(value.pk)
        except ValueError as e:
            raise IncorrectSecureModelFieldValue from e

    def to_python(self, value: str) -> db_models.Model | None:
        try:
            return super().to_python(reveal_int(value))
        except ValueError as e:
            raise IncorrectSecureModelFieldValue from e


def create_queryset_from_object(obj: Model) -> QuerySet:
    return obj.__class__.objects.all().filter(pk=obj.pk)
