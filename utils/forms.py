from typing import Literal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from django.db import models as db_models
from django.forms import models

from utils.common import generate_submit_type_button
from utils.crypto import hide_int, reveal_int


class SecureModelChoiceField(models.ModelChoiceField):
    __int_hider = staticmethod(hide_int)
    __int_revealer = staticmethod(reveal_int)

    def prepare_value(self, value: db_models.Model | None | Literal['']) -> str:
        if isinstance(value, db_models.Model):
            return self.__int_hider(value.pk)
        return super().prepare_value(value)

    def to_python(self, value: str | None) -> db_models.Model | None:
        if not value:
            return super().to_python(value)
        return super().to_python(self.__int_revealer(value))


def _reveal_id(hashed_id: str) -> int:
    """
    think twice before using, this function is supposed to be used when
    SecureModelChoiceField can not be used
    """
    _ = SecureModelChoiceField
    return _._SecureModelChoiceField__int_revealer(hashed_id)  # noqa pylint: disable=W0212


def _hide_id(_id: int) -> str:
    """
    think twice before using, this function is supposed to be used when
    SecureModelChoiceField can not be used
    """
    _ = SecureModelChoiceField
    return _._SecureModelChoiceField__int_hider(_id)  # noqa pylint: disable=W0212


class CrispyFormsMixin:
    """
    this mixin relies on crispy forms so form used with it heed to be displayed
    by corresponding crispy tag
    """

    def hide_fields(self):
        try:
            for field in self.Meta.fields_to_hide:  # noqa
                self.helper[field].wrap(Div, css_class="d-none")
        except AttributeError as e:
            raise AttributeError('your did not provide Meta class or fields_to_hide in it') from e

    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            self.helper = FormHelper(self)
        return self._helper

    @helper.setter
    def helper(self, value):
        self._helper = value

    def add_submit_button_at_the_end(self, text: str, value: str = 'submit', name: str = 'submit'):
        self.helper.layout.append(
            generate_submit_type_button(
                text,
                value,
                name
            )
        )

    @staticmethod
    def get_field_name(_field: Div | str) -> str:  # pylint: disable=W0238
        if isinstance(_field, str):
            return _field
        if len(_field.fields) != 1:
            raise ValueError('only one wrapped field expected')
        return _field.fields[0]


class IncorrectSecureModelFieldValue(Exception):
    pass
