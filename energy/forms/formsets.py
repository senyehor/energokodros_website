from django.forms import BaseFormSet, formset_factory

from energokodros.settings import SENSOR_COUNT_PER_BOX
from energy.forms.simple import BoxSensorsSetForm, SensorForm

__SensorsFormsetBase = formset_factory(
    SensorForm,
    # setting extra to zero as actual forms count will depend on data or initial
    extra=0,
    min_num=SENSOR_COUNT_PER_BOX,
    max_num=SENSOR_COUNT_PER_BOX,
)

__BoxSensorSetFormset = formset_factory(
    BoxSensorsSetForm,
    # setting extra to zero as actual forms count will depend on data or initial
    extra=0,
    min_num=SENSOR_COUNT_PER_BOX,
    max_num=SENSOR_COUNT_PER_BOX,
)


class __MustBeUsedWithInitialOrData:
    def __init__(self: BaseFormSet, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not any((self.initial, self.data)):
            raise ValueError('must be used either with data or initial')


class SensorsFormset(__MustBeUsedWithInitialOrData, __SensorsFormsetBase):
    pass


class BoxSensorSetFormset(__MustBeUsedWithInitialOrData, __BoxSensorSetFormset):
    pass
