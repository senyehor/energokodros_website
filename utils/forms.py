from typing import Any, Callable, Literal

from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div
from django.db.models import Model
from django.forms import models

from utils.crypto import IntHasher

INT_HIDER = IntHasher.hide_int
INT_REVEALER = IntHasher.reveal_int


class SecureModelChoiceField(models.ModelChoiceField):
    __int_hider = staticmethod(INT_HIDER)
    __int_revealer = staticmethod(INT_REVEALER)

    def prepare_value(self, value: Model | None | Literal['']) -> str:
        if isinstance(value, Model):
            return self.__int_hider(value.pk)
        return super().prepare_value(value)

    def to_python(self, value: str | None) -> Model | None:
        if value:
            return super().to_python(self.__int_revealer(value))
        return super().to_python(value)

    def __init__(
            self, queryset, *, empty_label="---------", required=True, widget=None, label=None,
            initial=None, help_text="", to_field_name=None, limit_choices_to=None, blank=False,
            label_from_instance_function: Callable[[Any], str] = None, **kwargs):
        super().__init__(
            queryset, empty_label=empty_label, required=required, widget=widget, label=label,
            initial=initial, help_text=help_text, to_field_name=to_field_name,
            limit_choices_to=limit_choices_to, blank=blank, **kwargs
        )
        self.label_from_instance_function = label_from_instance_function

    def label_from_instance(self, obj):
        if self.label_from_instance_function:
            return self.label_from_instance_function(obj)
        return super().label_from_instance(obj)


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
            self.__generate_submit_type_button(
                text,
                value,
                name
            )
        )

    def __generate_submit_type_button(self, text: str, value: str, name: str) -> StrictButton:
        return StrictButton(
            text,
            name=name,
            value=value,
            css_class='btn btn-primary mt-4',
            type='submit'
        )
