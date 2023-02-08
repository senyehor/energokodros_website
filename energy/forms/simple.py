from django.forms import (
    CharField, Textarea, TextInput,
)
from django.utils.translation import gettext_lazy as _

from energy.models import Box, BoxSensorSet, Sensor
from institutions.models import Facility
from utils.forms import (
    CrispyModelForm, SecureModelChoiceField, UPDATE_DELETE_BUTTONS_SET,
)


class SensorForm(CrispyModelForm):
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


class BoxForm(CrispyModelForm):
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
