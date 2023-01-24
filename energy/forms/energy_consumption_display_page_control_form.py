from django.forms import ChoiceField, Form
from django.utils.translation import gettext_lazy as _

from energy.logic.aggregated_consumption.models import AggregationIntervalSeconds
from institutions.models import Facility
from users.models import User, UserRole
from utils.forms import CrispyFormMixin, SecureModelChoiceField

AGGREGATION_INTERVAL_CHOICES = (
    (AggregationIntervalSeconds.ONE_HOUR.value, _('Година')),
    (AggregationIntervalSeconds.ONE_DAY.value, _('День')),
    (AggregationIntervalSeconds.ONE_WEEK.value, _('Тиждень')),
    (AggregationIntervalSeconds.ONE_MONTH.value, _('Місяць')),
    (AggregationIntervalSeconds.ONE_YEAR.value, _('Рік')),
)


class EnergyConsumptionDisplayPageControlForm(CrispyFormMixin, Form):
    """must be created for user using corresponding method,
    and some fields are added in the template"""
    # correct qs for role is set in __init__
    role = SecureModelChoiceField(
        label=_('Роль'),
        queryset=UserRole.objects.all(),
        empty_label=None,
    )
    # should be populated via ajax depending on chosen role,
    # qs is not as facility validation is done when querying for facilities list for role
    # field is used just for label and select widget
    facility_to_get_consumption_for = SecureModelChoiceField(
        label=_("Об'єкт"),
        queryset=Facility.objects.none(),
    )
    aggregation_interval_seconds = ChoiceField(
        label=_('Інтервал агрегації'),
        choices=AGGREGATION_INTERVAL_CHOICES,
    )

    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__set_correct_roles_choices(user)

    def __set_correct_roles_choices(self, user: User):
        self.fields['role'].queryset = user.roles
