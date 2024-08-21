from django.utils.translation import gettext as _

from utils.exceptions import ExceptionWithMessage


class EnergyConsumptionExceptionWithMessage(ExceptionWithMessage):
    pass


class InvalidHourFilteringMethod(EnergyConsumptionExceptionWithMessage):
    message = _('Такого методу погодинної фільтрації не існує')


class QueryParametersInvalid(EnergyConsumptionExceptionWithMessage):
    message = _('Сталася помилка при опрацюванні параметрів')


class FutureFilteringDate(EnergyConsumptionExceptionWithMessage):
    message = _('Фільтрація по майбутнім датам заборонена')


class AggregationIntervalDoesNotFitPeriod(EnergyConsumptionExceptionWithMessage):
    message = _('Обраний період не містить жодного інтервалу агрегації')


class PeriodStartGreaterThanEnd(EnergyConsumptionExceptionWithMessage):
    message = _('Початок періоду пізніше кінця')


class StartHourGreaterThanEndHour(EnergyConsumptionExceptionWithMessage):
    message = _('Початкова година фільтрації більша за кінцеву')


class ForecastForParametersDoesNotExist(EnergyConsumptionExceptionWithMessage):
    message = _('Для заданих параметрів прогноз відсутній')


class FacilityAndDescendantsHaveNoSensors(EnergyConsumptionExceptionWithMessage):
    message = _("У обраного об'єкту немає прив'язаних сенсорів")
