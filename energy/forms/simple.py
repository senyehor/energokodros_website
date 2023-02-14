from django.db.models import Model
from django.forms import CharField, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from energy.models import Box, BoxSensorSet, Sensor
from institutions.models import Facility
from utils.common.object_to_queryset import object_to_queryset
from utils.forms import CrispyModelForm, SecureModelChoiceField, UPDATE_DELETE_BUTTONS_SET
from utils.views import AdditionalSetupRequiredFormMixin


class SensorFormNoRelationFields(CrispyModelForm):
    sensor_description = CharField(
        label=_('Опис'),
        required=True,
        max_length=255,
    )

    class Meta:
        model = Sensor
        fields = ('sensor_number', 'sensor_description')
        labels = {
            'sensor_number': _('Власний номер'),
        }
        buttons = UPDATE_DELETE_BUTTONS_SET


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

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        sensor: Sensor = obj
        self.fields['box'].queryset = object_to_queryset(sensor.set.box)
        self.fields['set'].queryset = object_to_queryset(sensor.set)


class BoxFormNoRelationFields(CrispyModelForm):
    class Meta:
        model = Box
        fields = ('identifier', 'description')
        labels = {
            'identifier':  _('Ідентифікатор'),
            'description': _('Опис')
        }
        widgets = {
            'description': Textarea({'rows': '4'})
        }
        buttons = UPDATE_DELETE_BUTTONS_SET


class BoxSensorSetForm(CrispyModelForm):
    # sensor number must be prepopulated from created sensors
    sensor_number = CharField(
        label=_('Номер сенсора у наборі'),
        required=False,
        widget=TextInput(attrs={'readonly': 'readonly'})
    )
    facility = SecureModelChoiceField(
        label=_("Об'єкт сенсора"),
        # qs set to all to correctly process accept any facility,
        # correct choices must be set via ajax for to chosen institution
        queryset=Facility.objects.all(),
        required=True,
        empty_label=None
    )

    class Meta:
        model = BoxSensorSet
        fields = ('line_name', 'sensor_number_in_set')
        labels = {
            'line_name':            _('Назва лінії'),
            'sensor_number_in_set': _('Номер сенсора у ящику'),
        }
        fields_order = ('sensor_number',) + fields + ('facility',)
        buttons = UPDATE_DELETE_BUTTONS_SET
