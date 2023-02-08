from typing import Literal

from django.db.models import Model
from django.forms import models

from utils.crypto import IntHasher
from utils.forms.widgets import SelectWithFormControlClass

INT_HIDER = IntHasher.hide_int
INT_REVEALER = IntHasher.reveal_int


class SecureModelChoiceField(models.ModelChoiceField):
    __int_hider = staticmethod(INT_HIDER)
    __int_revealer = staticmethod(INT_REVEALER)
    widget = SelectWithFormControlClass()

    def prepare_value(self, value: Model | None | Literal['']) -> str:
        if isinstance(value, Model):
            return self.__int_hider(value.pk)
        return super().prepare_value(value)

    def to_python(self, value: str | None) -> Model | None:
        if value:
            return super().to_python(self.__int_revealer(value))
        return super().to_python(value)

    def __init__(self, *args, **kwargs):
        label_from_instance_function = kwargs.pop('label_from_instance_function', None)
        super().__init__(*args, **kwargs)
        self.label_from_instance_function = label_from_instance_function

    def label_from_instance(self, obj):
        if self.label_from_instance_function:
            return self.label_from_instance_function(obj)
        return super().label_from_instance(obj)
