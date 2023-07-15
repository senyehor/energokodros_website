from typing import Literal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from django.db import models as db_models
from django.forms import models

from utils.common import generate_submit_type_button
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


class CrispyFormsMixin:
    """
    this mixin relies on crispy forms so form used with it heed to be displayed
    by {% crispy form form.helper %}
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

    def add_button_at_the_end(self, text: str, value: str = 'submit'):
        self.helper.layout.append(
            generate_submit_type_button(
                text,
                value
            )
        )

    @staticmethod
    def _get_wrapped_field_name_if_div(_field: Div | str) -> str:
        if isinstance(_field, str):
            return _field
        if len(_field.fields) != 1:
            raise ValueError('only one wrapped field expected')
        return _field.fields[0]
