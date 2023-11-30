from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper


class CrispyFormsMixin:
    """
    this mixin relies on crispy forms so form used with it heed to be displayed
    by corresponding crispy tag
    """

    @property
    def helper(self) -> FormHelper:
        if not hasattr(self, '_helper'):
            self.helper = FormHelper(self)
        return self._helper

    @helper.setter
    def helper(self, value):
        # noinspection PyAttributeOutsideInit
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
