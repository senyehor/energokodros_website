from dataclasses import dataclass, field

import factory
from django.utils.decorators import classonlymethod
from factory import django

from energy.models import Box, BoxSensorsSet, Sensor
from institutions.models import Facility
from institutions.tests.factories import InstitutionFactory


class BoxFactory(django.DjangoModelFactory):
    box_number = factory.Sequence(lambda n: f'{n}')
    box_description = factory.Sequence(lambda n: f'box number {n} description')

    class Meta:
        model = Box


class SensorFactory(django.DjangoModelFactory):
    sensor_number = factory.Sequence(lambda n: f'{n}')
    sensor_description = factory.Sequence(lambda n: f'sensor number {n} description')

    class Meta:
        model = Sensor


@dataclass
class BoxSensorsSetData:
    facility: Facility
    box: Box
    sensors: list[Sensor] = field(default_factory=list)


class BoxSensorsSetManualFactory:
    """this is not a DjangoModelFactory, due to application logic"""
    __SENSORS_PER_BOX = 16

    @classonlymethod
    def generate(cls, facility: Facility = None,
                 initial_number_for_subfactories_sequences: int = 1) -> BoxSensorsSetData:
        box = BoxFactory(__sequence=initial_number_for_subfactories_sequences)
        if not facility:
            facility = InstitutionFactory(__sequence=initial_number_for_subfactories_sequences)
        data = BoxSensorsSetData(facility, box)
        for i in range(cls.__SENSORS_PER_BOX):
            sensor = SensorFactory()
            BoxSensorsSet(
                box=box,
                sensor=sensor,
                facility=facility,
                line_name=f'line number {i + 1}',
                sensor_number=i + 1
            ).save()
            data.sensors.append(sensor)
        return data
