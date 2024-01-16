from typing import TypeAlias

from django.utils.translation import gettext_lazy as _

from energokodros.settings import MAX_SENSOR_COUNT_PER_BOX
from utils.types import StrKeyDict

FormsetData: TypeAlias = list[StrKeyDict]


def create_initial_sensor_numbers_for_sensors_formset() -> FormsetData:
    return [
        {'sensor_number': sensor_number}
        for sensor_number in range(1, MAX_SENSOR_COUNT_PER_BOX + 1)
    ]


def create_initial_sensor_numbers_in_set_for_box_sensor_set_formset(
        sensors_formset_cleaned_data: FormsetData) -> FormsetData:
    return [
        {
            'sensor_number':        sensors_data['sensor_number'],
            'sensor_number_in_set': sensor_number_in_set,
            'line_name':            _(f'Лінія {sensor_number_in_set}')
        }
        for sensor_number_in_set, sensors_data in enumerate(sensors_formset_cleaned_data, start=1)
    ]
