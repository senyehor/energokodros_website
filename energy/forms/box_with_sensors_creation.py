from django.forms import BaseFormSet, Form, formset_factory
from django.utils.translation import gettext_lazy as _

from energokodros.settings import SENSOR_COUNT_PER_BOX
from energy.forms import BoxSensorSetForm, SensorFormNoRelationFields
from institutions.models import Facility
from utils.forms import CrispyFormMixin, SecureModelChoiceField

__SensorsFormsetBase = formset_factory(
    SensorFormNoRelationFields,
    # setting extra to zero as actual forms count will depend on data or initial
    extra=0,
    min_num=SENSOR_COUNT_PER_BOX,
    max_num=SENSOR_COUNT_PER_BOX,
)

__BoxSensorSetFormset = formset_factory(
    BoxSensorSetForm,
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
