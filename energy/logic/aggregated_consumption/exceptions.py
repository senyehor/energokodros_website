from django.utils.translation import gettext_lazy as _

from utils.exceptions import ExceptionWithMessage


class EnergyConsumptionExceptionWithMessage(ExceptionWithMessage):
    pass


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
