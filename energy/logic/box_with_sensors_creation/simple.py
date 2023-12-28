from typing import TypeAlias

from django.utils.translation import gettext_lazy as _

from energokodros.settings import MAX_SENSORS_COUNT_PER_BOX, MIN_SENSORS_COUNT_PER_BOX
from utils.types import StrKeyDict


class STEPS:
    BOX = 'box'
    SENSORS = 'sensors'
    BOX_SENSORS_SET = 'box_sensor_set'


FormsetData: TypeAlias = list[StrKeyDict]


def create_initial_sensor_numbers_for_sensors_formset(sensor_count: int) -> FormsetData:
    return _create_sensor_number_in_sensor_count_range_list_of_dicts(sensor_count)


def create_initial_sensor_numbers_in_set_for_box_sensor_set_formset(
        sensors_formset_cleaned_data: FormsetData) -> FormsetData:
    return [
        {
            'sensor_number':        _dict['sensor_number'],
            'sensor_number_in_set': sensor_number_in_set,
            'line_name':            _(f'Лінія {sensor_number_in_set}')
        }
        for sensor_number_in_set, _dict in enumerate(sensors_formset_cleaned_data, start=1)
    ]


def _create_sensor_number_in_sensor_count_range_list_of_dicts(
        sensor_count: int) -> list[StrKeyDict]:
    validate_sensors_count(sensor_count)
    return [
        {'sensor_number': sensor_number}
        for sensor_number in range(1, sensor_count + 1)
    ]


def validate_sensors_count(count: int):
    if MAX_SENSORS_COUNT_PER_BOX < count < MIN_SENSORS_COUNT_PER_BOX:
        raise ValueError("invalid sensors count number")
