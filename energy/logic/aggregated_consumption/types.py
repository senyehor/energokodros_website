from datetime import datetime
from decimal import Decimal
from typing import TypeAlias

RawConsumptionForecast: TypeAlias = float

RawConsumptionTime: TypeAlias = datetime | str
RawConsumptionValue: TypeAlias = Decimal
RawTotalConsumption: TypeAlias = Decimal
RawQueryRows = list[tuple[RawConsumptionTime, RawConsumptionValue, RawTotalConsumption]]

ConsumptionTime: TypeAlias = str
ConsumptionValue: TypeAlias = str
ConsumptionForecast: TypeAlias = str
TotalConsumption: TypeAlias = str

RawConsumption = list[tuple[RawConsumptionTime, RawConsumptionValue]]
RawConsumptionWithRawTotalConsumption = tuple[
    RawConsumption, RawTotalConsumption
]
ConsumptionRow: TypeAlias = tuple[ConsumptionTime, ConsumptionValue]
Consumption: TypeAlias = list[ConsumptionRow]
ConsumptionWithFormattedTimeAndRawValueRow = tuple[ConsumptionTime, RawConsumption]
ConsumptionWithFormattedTimeAndRawValue: TypeAlias = list[
    ConsumptionWithFormattedTimeAndRawValueRow
]
ConsumptionWithConsumptionForecast: TypeAlias = \
    list[tuple[ConsumptionTime, ConsumptionValue, ConsumptionForecast]]
ConsumptionWithTotalConsumption = tuple[
    Consumption, TotalConsumption
]
ConsumptionWithConsumptionForecastWithTotalConsumption = tuple[
    ConsumptionWithConsumptionForecast, TotalConsumption
]

HOUR: TypeAlias = int
