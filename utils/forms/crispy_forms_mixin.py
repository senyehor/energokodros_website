from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div


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
    def helper(self) -> FormHelper:
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
