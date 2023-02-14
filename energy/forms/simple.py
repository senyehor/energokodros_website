from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from energy.forms import BoxFormNoRelationFields
from energy.forms.box_with_sensors_creation import SensorFormNoRelationFields
from energy.models import Box, BoxSensorSet, Sensor
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
