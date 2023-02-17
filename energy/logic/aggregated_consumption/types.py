from _decimal import Decimal
from datetime import datetime

from typing import TypeAlias

ConsumptionForecast: TypeAlias = float
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
RawAggregatedConsumptionDataWithForecast: TypeAlias = \
    list[tuple[RawConsumptionTime, RawConsumptionValue, ConsumptionForecast]]

HOUR: TypeAlias = int
