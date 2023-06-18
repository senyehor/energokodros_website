import re


def _full_name_validator(full_name: str) -> bool:
    valid_full_name_part_pattern = r'''[А-ЩЬЮЯҐЄІЇа-щьюяґєії'`’ʼ-]{2,40}'''
    full_name_pattern = '^' + r'\s'.join([valid_full_name_part_pattern] * 3) + '$'
    return bool(re.match(full_name_pattern, full_name))
