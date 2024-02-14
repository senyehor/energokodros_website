from typing import Iterable

from django.db import IntegrityError
from django.forms import Form

from energokodros.settings import SENSOR_COUNT_PER_BOX
from energy.forms import (
    BoxFormNoRelationFields, BoxSensorSetForBoxWithSensorsCreationForm,
    BoxSensorSetFormset, SensorFormNoRelationFields, SensorsFormset,
)
from energy.logic.box_with_sensors_creation.config_and_models import FORMS_ORDER_FROM_ZERO, STEPS
from energy.models import Box, BoxSensorSet, Sensor
from institutions.models import Facility


def create_box_sensor_sets_along_with_box_and_sensors(
        box_form: BoxFormNoRelationFields, sensors_formset: SensorsFormset,
        box_sensor_set_formset: BoxSensorSetFormset
):
    box = box_form.save()
    _ = create_box_sensor_set_form_and_sensor_form_match(box_sensor_set_formset, sensors_formset)
    for box_sensor_set_form, sensor_form in _:
        sensor: Sensor = sensor_form.save()
        box_sensor_set: BoxSensorSet = box_sensor_set_form.save(commit=False)
        facility = box_sensor_set_form.cleaned_data['facility']
        fill_box_sensor_set_relations(box_sensor_set, box, facility, sensor)
        box_sensor_set.save()
    box.refresh_from_db()
    validate_sensors_count(box)


def create_box_sensor_set_form_and_sensor_form_match(
        box_sensor_set_formset: BoxSensorSetFormset, sensors_formset: SensorsFormset
) -> Iterable[tuple[BoxSensorSetForBoxWithSensorsCreationForm, SensorFormNoRelationFields]]:
    return zip(box_sensor_set_formset.forms, sensors_formset.forms)


def fill_box_sensor_set_relations(
        box_sensor_set: BoxSensorSet, box: Box, facility: Facility, sensor: Sensor
) -> BoxSensorSet:
    box_sensor_set.facility = facility
    box_sensor_set.sensor = sensor
    box_sensor_set.box = box
    return box_sensor_set


def get_forms_from_from_list(forms: list[Form]) -> \
        tuple[BoxFormNoRelationFields, SensorsFormset, BoxSensorSetFormset]:
    # noinspection PyTypeChecker
    return (
        forms[FORMS_ORDER_FROM_ZERO[STEPS.BOX]],
        forms[FORMS_ORDER_FROM_ZERO[STEPS.SENSORS]],
        forms[FORMS_ORDER_FROM_ZERO[STEPS.BOX_SENSORS_SET]],
    )


def validate_sensors_count(box: Box):
    if box.sensor_sets.count() != SENSOR_COUNT_PER_BOX:
        raise IntegrityError('Invalid sensor count')
