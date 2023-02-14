from django.forms import BaseFormSet, CharField, Form, formset_factory, Textarea, TextInput
from django.utils.translation import gettext_lazy as _

from energokodros.settings import SENSOR_COUNT_PER_BOX
from energy.models import Box, BoxSensorSet, Sensor
from institutions.models import Facility
from utils.forms import (
    CrispyFormMixin, CrispyModelForm, SecureModelChoiceField,
)


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


__SensorsFormsetBase = formset_factory(
    SensorFormNoRelationFields,
    # setting extra to zero as actual forms count will depend on data or initial
    extra=0,
    min_num=SENSOR_COUNT_PER_BOX,
    max_num=SENSOR_COUNT_PER_BOX,
)


class BoxSensorSetForBoxWithSensorsCreationForm(CrispyModelForm):
    # sensor number must be prepopulated from created sensors
    sensor_number = CharField(
        label=_('Номер сенсора'),
        required=False,
        widget=TextInput(attrs={'readonly': 'readonly'})
    )
    facility = SecureModelChoiceField(
        label=_("Об'єкт сенсора"),
        # qs set to all to accept any facility,
        # correct choices must be set via ajax
        queryset=Facility.objects.all(),
        required=True,
        empty_label=None
    )

    class Meta:
        model = BoxSensorSet
        fields = ('line_name', 'sensor_number_in_set')
        labels = {
            'line_name':            _('Назва лінії'),
            'sensor_number_in_set': _('Номер сенсора наборі'),
        }
        fields_order = ('sensor_number',) + fields + ('facility',)


__BoxSensorSetFormset = formset_factory(
    BoxSensorSetForBoxWithSensorsCreationForm,
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


class ChooseInstitutionForm(CrispyFormMixin, Form):
    institution = SecureModelChoiceField(
        queryset=Facility.objects.get_institutions(),
        required=False,
        label=_("Оберіть заклад якому буде належати ящик"),
        empty_label=None,
    )
