from typing import Tuple

from django.contrib import messages
from django.db import transaction
from django.forms import Form
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from formtools.wizard.views import SessionWizardView

from energy.forms import (
    BoxForm, BoxSensorSetFormset, BoxSensorsSetForm, ChooseInstitutionForm, SensorsFormset,
)
from energy.logic.box_with_sensors_creation import (
    create_initial_sensor_numbers_for_sensors_formset,
    create_initial_sensor_numbers_in_set_for_box_sensor_set_formset,
    FormsetData,
)
from utils.common import admin_rights_and_login_required
from utils.types import StrKeyDict


class STEPS:
    BOX = 'box'
    SENSORS = 'sensors'
    BOX_SENSORS_SET = 'box_sensor_set'


FORMS = (
    (STEPS.BOX, BoxForm),
    # default sensors count is max but can be adjusted by user
    (STEPS.SENSORS, SensorsFormset),
    # box_sensors_set should be created dynamically depending on sensor count from previous step
    (STEPS.BOX_SENSORS_SET, BoxSensorSetFormset)
)

TEMPLATES = {
    STEPS.BOX:             'energy/box_with_sensors_creation/box.html',
    STEPS.SENSORS:         'energy/box_with_sensors_creation/sensors.html',
    STEPS.BOX_SENSORS_SET: 'energy/box_with_sensors_creation/box_sensors_set.html',
}

FORMS_ORDER_FROM_ZERO = {
    STEPS.BOX:             0,
    STEPS.SENSORS:         1,
    STEPS.BOX_SENSORS_SET: 2
}


@admin_rights_and_login_required
class BoxWithSensorsCreateView(SessionWizardView):
    form_list = FORMS
    # todo to list instead of home
    success_url = reverse_lazy('home')
    success_message = _('Успішно створено ящик та сенсори')

    @method_decorator(transaction.atomic)
    def done(self, form_list, **kwargs):
        box_form, sensors_formset, box_sensor_set_formset = self.__get_forms_from_form_list(
            form_list
        )
        box = box_form.save()
        for box_sensor_set_form, sensor_form in \
                zip(box_sensor_set_formset.forms, sensors_formset.forms):
            box_sensor_set_form: BoxSensorsSetForm = box_sensor_set_form
            sensor = sensor_form.save()
            box_sensor_set = box_sensor_set_form.save(commit=False)
            box_sensor_set.facility = box_sensor_set_form.cleaned_data['facility']
            box_sensor_set.sensor = sensor
            box_sensor_set.box = box
            box_sensor_set.save()
        messages.success(
            self.request,
            self.success_message
        )
        return redirect(self.success_url)

    def __get_forms_from_form_list(self, form_list: list[Form]) -> \
            Tuple[BoxForm, SensorsFormset, BoxSensorSetFormset]:
        # noinspection PyTypeChecker
        return (
            form_list[FORMS_ORDER_FROM_ZERO[STEPS.BOX]],
            form_list[FORMS_ORDER_FROM_ZERO[STEPS.SENSORS]],
            form_list[FORMS_ORDER_FROM_ZERO[STEPS.BOX_SENSORS_SET]],
        )

    def __create_box_sensor_set_initial(self) -> FormsetData:
        return create_initial_sensor_numbers_in_set_for_box_sensor_set_formset(
            self.get_cleaned_data_for_step(STEPS.SENSORS)
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)
        if self.steps.current == STEPS.BOX_SENSORS_SET:
            ctx.update(self.__create_institutions_choice_context_dict())
        return ctx

    def __create_institutions_choice_context_dict(self) -> StrKeyDict:
        return {
            'choose_institution_form': ChooseInstitutionForm()
        }

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        if step == STEPS.SENSORS:
            return create_initial_sensor_numbers_for_sensors_formset()
        if step == STEPS.BOX_SENSORS_SET:
            return self.__create_box_sensor_set_initial()
        return {}
