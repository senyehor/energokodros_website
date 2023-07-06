from typing import Literal

from django.db import models as db_models
from django.forms import models

from utils.crypto import hide_int, reveal_int


class SecureModelChoiceField(models.ModelChoiceField):

    def prepare_value(self, value: db_models.Model | None | Literal['']) -> str:
        if not value:
            return super().to_python(value)
        return hide_int(value.pk)

    def to_python(self, value: str) -> db_models.Model:
        return super().to_python(reveal_int(value))
