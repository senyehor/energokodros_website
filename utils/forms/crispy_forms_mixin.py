from typing import Iterable

from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from django.forms import Form, ModelForm


class CrispyFormMixin:
    """
    provides unified way to make form crispy‚
    relies on crispy forms so form used with it heed to be displayed
    by corresponding crispy tag
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__order_fields_if_present()
        self.helper = FormHelper(self)
        self.__add_buttons()

    def __add_buttons(self):
        try:
            # noinspection PyUnresolvedReferences
            buttons: Iterable[StrictButton] = self.Meta.buttons
        except AttributeError:
            return
        for button in buttons:
            self.helper.layout.append(button)

    def __order_fields_if_present(self: Form):
        try:
            # noinspection PyUnresolvedReferences
            self.order_fields(self.Meta.fields_order)
        except AttributeError:
            return

    def add_button(self, button: StrictButton):
        self.helper.layout.append(button)


class CrispyModelForm(CrispyFormMixin, ModelForm):
    pass
