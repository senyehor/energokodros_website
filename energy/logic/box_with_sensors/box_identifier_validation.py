import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

__CITY_REGEX_PART = '[A-Za-z]{2}'
__INSTITUTION_NAME_REGEX_PART = '[A-Za-z]{2}'
__INSTITUTION_NUMBER_REGEX_PART = r'\d{2}'
__BOX_NUMBER_REGEX_PART = r'\d{3}'
__BOX_ACTUAL_SENSOR_COUNT_REGEX_PART = r'\d{2}'

__COMPOSED_REGEX = re.compile(
    fr'^{__CITY_REGEX_PART}' +
    fr'{__INSTITUTION_NUMBER_REGEX_PART}' +
    fr'{__INSTITUTION_NUMBER_REGEX_PART}' +
    fr'{__BOX_NUMBER_REGEX_PART}' +
    fr'{__BOX_ACTUAL_SENSOR_COUNT_REGEX_PART}$'
)


def validate_box_identifier(identifier: str):
    if not __COMPOSED_REGEX.match(identifier):
        raise ValidationError(
            _('Ідентифікатор не відповідає заданому формату')
        )
