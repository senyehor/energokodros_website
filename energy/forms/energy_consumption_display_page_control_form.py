from django.forms import ChoiceField, Form
from django.utils.translation import gettext_lazy as _

from energy.logic.aggregated_energy_consumption_query_builder import AggregationIntervalInSeconds
from institutions.models import Facility
from users.models import User, UserRole
from utils.forms import CrispyFormsMixin, SecureModelChoiceField

AGGREGATION_INTERVAL_CHOICES = (
    (AggregationIntervalInSeconds.ONE_HOUR.value, _('Година')),
    (AggregationIntervalInSeconds.ONE_DAY.value, _('День')),
    (AggregationIntervalInSeconds.ONE_WEEK.value, _('Тиждень')),
    (AggregationIntervalInSeconds.ONE_MONTH.value, _('Місяць')),
    (AggregationIntervalInSeconds.ONE_YEAR.value, _('Рік')),
)


class EnergyConsumptionDisplayPageControlForm(Form, CrispyFormsMixin):
    """must be created for user using dedicated method"""
    # correct qs is set in __init__
    role = SecureModelChoiceField(
        queryset=UserRole.objects.all(),
        empty_label=None,
        label=_('Роль')
    )
    # should be populated via ajax depending on chosen role
    facility_to_get_consumption_for = SecureModelChoiceField(
        queryset=Facility.objects.all(),
        label=_("Об'єкт")
    )
    aggregation_interval_seconds = ChoiceField(
        choices=AGGREGATION_INTERVAL_CHOICES,
        label=_('Інтервал агрегації')
    )

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_correct_roles_choices(user)

    def __set_correct_roles_choices(self, user: User):
        self.fields['role'].queryset = user.roles
