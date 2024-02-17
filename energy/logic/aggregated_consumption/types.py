from _decimal import Decimal
from datetime import datetime

from typing import TypeAlias

RawConsumptionForecast: TypeAlias = float
RawConsumptionTime: TypeAlias = datetime | str
RawConsumptionValue: TypeAlias = Decimal

FormattedConsumptionTime: TypeAlias = str
FormattedConsumptionValue: TypeAlias = str
FormattedConsumptionForecast: TypeAlias = str

RawAggregatedConsumptionData = list[tuple[RawConsumptionTime, RawConsumptionValue]]
AggregatedConsumptionData: TypeAlias = \
    list[
        tuple[FormattedConsumptionTime, FormattedConsumptionValue]
    ]
AggregatedConsumptionDataWithForecast: TypeAlias = \
    list[tuple[FormattedConsumptionTime, FormattedConsumptionValue, FormattedConsumptionForecast]]

HOUR: TypeAlias = int
