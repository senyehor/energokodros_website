from enum import Enum

REGEX_GROUPS_SEPARATOR = '-'


class CharactersCountForBoxIdentifierParts:
    CHARACTERS_PER_BOX_ORDINAL_NUMBER_FOR_BOX_IDENTIFIER = 2
    CHARACTERS_PER_CITY_FOR_BOX_IDENTIFIER = 2
    CHARACTERS_PER_INSTITUTION_FOR_BOX_IDENTIFIER = 2
    CHARACTERS_PER_INSTITUTION_NUMBER_FOR_BOX_IDENTIFIER = 2
    CHARACTERS_PER_SENSORS_COUNT_FOR_BOX_IDENTIFIER = 2


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
    groups = BoxIdentifierRegexGroups
    _ = CharactersCountForBoxIdentifierParts
    city = create_regex_for_letter_count(
        groups.CITY,
        _.CHARACTERS_PER_CITY_FOR_BOX_IDENTIFIER
    )
    institution = create_regex_for_letter_count(
        groups.INSTITUTION,
        _.CHARACTERS_PER_INSTITUTION_FOR_BOX_IDENTIFIER
    )
    institution_number = create_regex_for_number_count(
        groups.INSTITUTION_NUMBER,
        _.CHARACTERS_PER_INSTITUTION_NUMBER_FOR_BOX_IDENTIFIER
    )
    box_ordinal_number = create_regex_for_number_count(
        groups.BOX_ORDINAL_NUMBER,
        _.CHARACTERS_PER_BOX_ORDINAL_NUMBER_FOR_BOX_IDENTIFIER
    )
    sensors_count = create_regex_for_number_count(
        groups.SENSORS_COUNT,
        _.CHARACTERS_PER_SENSORS_COUNT_FOR_BOX_IDENTIFIER
    )
    return REGEX_GROUPS_SEPARATOR.join(
        (
            city, institution, institution_number, box_ordinal_number, sensors_count
        )
    )
