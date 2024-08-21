class EnergyConsumptionLogicException(Exception):
    """
    Base for exceptions for unexpected and possibly malicious actions from user,
    such as manually sending wrong or incomplete data etc
    """


class InvalidHourFilteringValue(EnergyConsumptionLogicException):
    pass


class IncompleteHourFiltersSet(EnergyConsumptionLogicException):
    pass
