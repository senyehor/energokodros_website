class EnergyConsumptionLogicException(Exception):
    """
    Base for exceptions for unexpected and possibly malicious actions from user,
    such as manually sending wrong or incomplete data etc
    """


class InvalidIncludeForecastValue(EnergyConsumptionLogicException):
    pass


class InvalidHourFilteringValue(EnergyConsumptionLogicException):
    pass


class IncompleteHourFiltersSet(EnergyConsumptionLogicException):
    pass


class MonthPeriodStartDoesNotBeginWithFirstMonthDay(EnergyConsumptionLogicException):
    pass


class MonthPeriodEndDoesNotEndWithLastMonthDay(EnergyConsumptionLogicException):
    pass
