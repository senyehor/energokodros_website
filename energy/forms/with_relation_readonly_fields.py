from django.db.models import Model
from django.utils.translation import gettext as _

from energy.forms.simple import SensorForm
from energy.models import Box, BoxSensorSet, Sensor
from utils.common.object_to_queryset import object_to_queryset
from utils.forms import SecureModelChoiceField
from utils.views import AdditionalSetupRequiredFormMixin


class SensorFormWithBoxAndSetFields(SensorForm, AdditionalSetupRequiredFormMixin):
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

    class Meta(SensorForm.Meta):
        fields_order = SensorForm.Meta.fields + ('box', 'set')

    def additionally_setup(self, obj: Model):
        # noinspection PyTypeChecker
        sensor: Sensor = obj
        self.fields['box'].queryset = object_to_queryset(sensor.set.box)
        self.fields['set'].queryset = object_to_queryset(sensor.set)
