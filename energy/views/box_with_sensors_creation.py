from django.contrib import messages
from django.db import transaction
from django.forms import Form
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from formtools.wizard.views import SessionWizardView

from energy.forms import ChooseInstitutionForm
from energy.logic.box_with_sensors_creation import (
    BOX_WITH_SENSORS_CREATION_TEMPLATES, create_box_sensor_sets_along_with_box_and_sensors,
    create_initial_sensor_numbers_for_sensors_formset,
    create_initial_sensor_numbers_in_set_for_box_sensor_set_formset, FORMS, FormsetData,
    get_forms_from_from_list, STEPS,
)
from utils.common import admin_rights_and_login_required
from utils.types import StrKeyDict


@admin_rights_and_login_required
class BoxWithSensorsCreateView(SessionWizardView):
    form_list = FORMS
    success_url = reverse_lazy('box-list')
    success_message = _('Успішно створено ящик та сенсори')

    @method_decorator(transaction.atomic)
    def done(self, form_list, **kwargs):
        box_form, sensors_formset, box_sensor_set_formset = self.__get_forms_from_form_list(
            form_list
        )
        create_box_sensor_sets_along_with_box_and_sensors(
            box_form, sensors_formset, box_sensor_set_formset
        )
        messages.success(
            self.request,
            self.success_message
        )
        return redirect(self.success_url)

    def __get_forms_from_form_list(self, forms: list[Form]):
        return get_forms_from_from_list(forms)

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
        return [BOX_WITH_SENSORS_CREATION_TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        if step == STEPS.SENSORS:
            return create_initial_sensor_numbers_for_sensors_formset()
        if step == STEPS.BOX_SENSORS_SET:
            return self.__create_box_sensor_set_initial()
        return {}
