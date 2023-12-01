from typing import Tuple

from crispy_forms.bootstrap import StrictButton
from django.utils.translation import gettext as _

COMMON_CSS_CLASSES = 'btn mt-4'
DEFAULT_BUTTON_VALUE = 'submit'
DEFAULT_BUTTON_NAME = 'submit'
DEFAULT_BUTTON_TYPE = 'submit'
DEFAULT_DELETE_VALUE = 'delete'
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
        css_class=' '.join(additional_css_classes + (COMMON_CSS_CLASSES,))
    )


def __add_classes_for_button(kwargs: dict, classes_to_add: StrTuple) -> dict:
    additional_css_classes = kwargs.get('additional_css_classes', None)
    if additional_css_classes:
        additional_css_classes += classes_to_add
    else:
        additional_css_classes = classes_to_add
    kwargs['additional_css_classes'] = additional_css_classes
    return kwargs


def create_primary_button(*args, **kwargs):
    kwargs = __add_classes_for_button(kwargs, ('btn-primary',))
    return create_button(*args, **kwargs)


def create_danger_button(*args, **kwargs):
    kwargs = __add_classes_for_button(kwargs, ('btn-danger',))
    return create_button(*args, **kwargs)


UPDATE_DELETE_BUTTONS_SET = (
    create_primary_button(_('Оновити')),
    create_danger_button(_('Видалити'), value=DEFAULT_DELETE_VALUE)
)
