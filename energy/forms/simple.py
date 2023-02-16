from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from energy.forms.box_with_sensors_creation import (
    BoxFormNoRelationFields,
    BoxSensorSetForBoxWithSensorsCreationForm, SensorFormNoRelationFields,
)
from energy.models import Box, BoxSensorSet, Sensor
from institutions.logic import (
    common_facility_choices_format_function, get_all_facilities_of_facility_institution,
)
from institutions.models import Facility
from utils.common.object_to_queryset import object_to_queryset
from utils.forms import (
    SecureModelChoiceField, SelectWithFormControlClass,
    UPDATE_DELETE_BUTTONS_SET,
)
from utils.views import AdditionalSetupRequiredFormMixin


class SensorForm(SensorFormNoRelationFields, AdditionalSetupRequiredFormMixin):
    box = SecureModelChoiceField(
        queryset=Box.objects.none(),
        label=_('Ящик'),
        empty_label=None,
        disabled=True
    )
    set = SecureModelChoiceField(
        queryset=BoxSensorSet.objects.none(),
        label=_('Набір'),
        empty_label=None,
        disabled=True
    )

    class Meta(SensorFormNoRelationFields.Meta):
        fields_order = SensorFormNoRelationFields.Meta.fields + ('box', 'set')
        buttons = UPDATE_DELETE_BUTTONS_SET

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        sensor: Sensor = obj
        self.fields['box'].queryset = object_to_queryset(sensor.set.box)
        self.fields['set'].queryset = object_to_queryset(sensor.set)


class BoxForm(BoxFormNoRelationFields, AdditionalSetupRequiredFormMixin):
    sensor_sets = SecureModelChoiceField(
        queryset=BoxSensorSet.objects.none(),
        disabled=True,
        label=_('Набори'),
        label_from_instance_function=lambda _set: _(f'Набір {_set.sensor_number_in_set}'),
        widget=SelectWithFormControlClass(attrs={'size': 10}),
        empty_label=None
    )

    class Meta(BoxFormNoRelationFields.Meta):
        buttons = UPDATE_DELETE_BUTTONS_SET

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        box: Box = obj
        self.fields['sensor_sets'].queryset = box.sensor_sets


class BoxSensorSetForm(BoxSensorSetForBoxWithSensorsCreationForm, AdditionalSetupRequiredFormMixin):
    # sensor number is model choice field in order to have sensor pk in form
    # so user can be easily redirected to sensor page
    sensor_number = SecureModelChoiceField(
        label=_('Номер сенсора'),
        # correct sensor must be set in additionally_setup
        queryset=Sensor.objects.all(),
        label_from_instance_function=lambda x: x.sensor_number,
        empty_label=None,
        disabled=True,
        required=False
    )
    facility = SecureModelChoiceField(
        label=_("Об'єкт сенсора"),
        # qs set to all to accept any facility,
        # correct choices must be set in additionally_setup
        queryset=Facility.objects.all(),
        empty_label=None,
        label_from_instance_function=common_facility_choices_format_function
    )

    class Meta(BoxSensorSetForBoxWithSensorsCreationForm.Meta):
        buttons = UPDATE_DELETE_BUTTONS_SET

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        box_sensor_set: BoxSensorSet = obj
        self.fields['sensor_number'].queryset = object_to_queryset(box_sensor_set.sensor)
        self.fields['facility'].queryset = \
            get_all_facilities_of_facility_institution(box_sensor_set.facility)
        self.fields['facility'].initial = box_sensor_set.facility
