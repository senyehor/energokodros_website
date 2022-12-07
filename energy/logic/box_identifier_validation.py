from enum import Enum

from energokodros.settings import (
    CHARACTERS_PER_BOX_ORDINAL_NUMBER_FOR_BOX_IDENTIFIER, CHARACTERS_PER_CITY_FOR_BOX_IDENTIFIER,
    CHARACTERS_PER_INSTITUTION_FOR_BOX_IDENTIFIER,
    CHARACTERS_PER_INSTITUTION_NUMBER_FOR_BOX_IDENTIFIER,
    CHARACTERS_PER_SENSORS_COUNT_FOR_BOX_IDENTIFIER,
)

REGEX_GROUPS_SEPARATOR = '-'


class BoxIdentifierRegexGroups(str, Enum):
    CITY = 'city'
    INSTITUTION = 'institution'
    INSTITUTION_NUMBER = 'institution_number'
    BOX_ORDINAL_NUMBER = 'box_ordinal_number'
    SENSORS_COUNT = 'sensors_count'


def create_regex_for_letter_count(group_name: str, count: int) -> str:
    return f'(?P<{group_name}>[A-Za-z]{{{count}}})'


def create_regex_for_number_count(group_name: str, count: int) -> str:
    return f'(?P<{group_name}>[0-9]{{{count}}})'


def compose_regex() -> str:
    _ = BoxIdentifierRegexGroups
    city = create_regex_for_letter_count(
        _.CITY,
        CHARACTERS_PER_CITY_FOR_BOX_IDENTIFIER
    )
    institution = create_regex_for_letter_count(
        _.INSTITUTION,
        CHARACTERS_PER_INSTITUTION_FOR_BOX_IDENTIFIER
    )
    institution_number = create_regex_for_number_count(
        _.INSTITUTION_NUMBER,
        CHARACTERS_PER_INSTITUTION_NUMBER_FOR_BOX_IDENTIFIER
    )
    box_ordinal_number = create_regex_for_number_count(
        _.BOX_ORDINAL_NUMBER,
        CHARACTERS_PER_BOX_ORDINAL_NUMBER_FOR_BOX_IDENTIFIER
    )
    sensors_count = create_regex_for_number_count(
        _.SENSORS_COUNT,
        CHARACTERS_PER_SENSORS_COUNT_FOR_BOX_IDENTIFIER
    )
    return REGEX_GROUPS_SEPARATOR.join(
        (
            city, institution, institution_number, box_ordinal_number, sensors_count
        )
    )
