from typing import Tuple

from crispy_forms.bootstrap import StrictButton

COMMON_CSS_CLASSES = 'btn mt-4'
DEFAULT_BUTTON_VALUE = 'submit'
DEFAULT_BUTTON_NAME = 'submit'
DEFAULT_BUTTON_TYPE = 'submit'
StrTuple = Tuple[str, ...]


def create_button(
        text: str, *, value: str = DEFAULT_BUTTON_VALUE, name: str = DEFAULT_BUTTON_NAME,
        button_type: str = DEFAULT_BUTTON_TYPE, additional_css_classes: StrTuple = ()
) -> StrictButton:
    return StrictButton(
        text,
        value=value,
        name=name,
        type=button_type,
        css_class=COMMON_CSS_CLASSES + ' '.join(additional_css_classes)
    )


def __add_classes_for_button(kwargs: dict, classes_to_add: StrTuple) -> dict:
    kwargs['additional_css_classes'] = kwargs['additional_css_classes'] + classes_to_add
    return kwargs


def create_primary_button(*args, **kwargs):
    kwargs = __add_classes_for_button(kwargs, ('btn-primary',))
    return create_button(*args, **kwargs)


def create_danger_button(*args, **kwargs):
    kwargs = __add_classes_for_button(kwargs, ('btn-danger',))
    return create_button(*args, **kwargs)
