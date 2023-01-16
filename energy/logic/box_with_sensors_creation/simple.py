from typing import Iterable, Tuple

from django.forms import Form

from energokodros.settings import MAX_SENSOR_COUNT_PER_BOX, MIN_SENSOR_COUNT_PER_BOX
from energy.forms import BoxForm, BoxSensorSetFormset, BoxSensorsSetForm, SensorForm, SensorsFormset
from energy.logic.box_with_sensors_creation.config_and_models import FORMS_ORDER_FROM_ZERO, STEPS
from energy.models import Box, BoxSensorsSet, Sensor
from institutions.models import Facility


def create_box_sensor_sets_along_with_box_and_sensors(
        box_form: BoxForm, sensors_formset: SensorsFormset,
        box_sensor_set_formset: BoxSensorSetFormset
):
    box = box_form.save()
    _ = create_box_sensor_set_form_and_sensor_form_match(box_sensor_set_formset, sensors_formset)
    for box_sensor_set_form, sensor_form in _:
        sensor = sensor_form.save()
        box_sensor_set = box_sensor_set_form.save(commit=False)
        facility = box_sensor_set.cleaned_data['facility']
        fill_box_sensor_set_relations(box_sensor_set, box, facility, sensor)
        box_sensor_set.save()


def create_box_sensor_set_form_and_sensor_form_match(
        box_sensor_set_formset: BoxSensorSetFormset, sensors_formset: SensorsFormset) -> \
        Iterable[Tuple[BoxSensorsSetForm, SensorForm]]:
    return zip(box_sensor_set_formset.forms, sensors_formset.forms)


def fill_box_sensor_set_relations(
        box_sensor_set: BoxSensorsSet, box: Box, facility: Facility, sensor: Sensor
) -> BoxSensorsSet:
    box_sensor_set.facility = facility
    box_sensor_set.sensor = sensor
    box_sensor_set.box = box
    return box_sensor_set


def get_forms_from_from_list(forms: list[Form]) -> \
        Tuple[BoxForm, SensorsFormset, BoxSensorSetFormset]:
    # noinspection PyTypeChecker
    return (
        forms[FORMS_ORDER_FROM_ZERO[STEPS.BOX]],
        forms[FORMS_ORDER_FROM_ZERO[STEPS.SENSORS]],
        forms[FORMS_ORDER_FROM_ZERO[STEPS.BOX_SENSORS_SET]],
    )


def validate_sensors_count(count: int):
    if MAX_SENSOR_COUNT_PER_BOX < count < MIN_SENSOR_COUNT_PER_BOX:
        raise ValueError("invalid sensors count number")