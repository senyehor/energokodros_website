import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def _full_name_validator(full_name: str):
    valid_full_name_part_pattern = r'''[А-ЩЬЮЯҐЄІЇа-щьюяґєії'`’ʼ-]{2,40}'''
    full_name_pattern = '^' + r'\s'.join([valid_full_name_part_pattern] * 3) + '$'
    if not bool(re.match(full_name_pattern, full_name)):
        raise ValidationError(_("Некоректне ім'я."))
