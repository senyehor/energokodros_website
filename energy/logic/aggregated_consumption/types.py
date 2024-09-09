from datetime import datetime
from decimal import Decimal
from typing import Iterable, NamedTuple, TypeAlias

RawConsumptionValue: TypeAlias = Decimal
RawConsumptionTime: TypeAlias = datetime | str


class RawConsumption(NamedTuple):
    time: RawConsumptionTime
    value: RawConsumptionValue


RawConsumptionForecast: TypeAlias = float
RawTotalConsumption: TypeAlias = Decimal
RawQueryRows = Iterable[
    tuple[type(RawConsumption.time), type(RawConsumption.value), RawTotalConsumption]
]

ConsumptionTime: TypeAlias = str
ConsumptionValue: TypeAlias = str
ConsumptionForecast: TypeAlias = str
TotalConsumption: TypeAlias = str

RawConsumptionWithRawTotalConsumption = tuple[
    Iterable[RawConsumption], RawTotalConsumption
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
