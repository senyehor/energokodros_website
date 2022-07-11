from typing import Literal

from django.core.exceptions import SuspiciousOperation
from django.db import models as db_models
from django.forms import models

from utils.crypto import hide_int, reveal_int


class SecureModelChoiceField(models.ModelChoiceField):

    def prepare_value(self, value: db_models.Model | None | Literal['']) -> str:
        if not value:
            return super().to_python(value)
        try:
            return hide_int(value.pk)
        except ValueError:
            raise SuspiciousOperation

    def to_python(self, value: str) -> db_models.Model:
        try:
            return super().to_python(reveal_int(value))
        except ValueError:
            raise SuspiciousOperation
