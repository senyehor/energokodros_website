from datetime import datetime
from decimal import Decimal
from typing import Iterable, NamedTuple, TypeAlias

RawConsumptionValue: TypeAlias = Decimal
RawConsumptionTime: TypeAlias = datetime | str


class RawConsumptionRecord(NamedTuple):
    time: RawConsumptionTime
    value: RawConsumptionValue


RawConsumptionForecast: TypeAlias = float
RawTotalConsumption: TypeAlias = Decimal
RawQueryRows = Iterable[
    tuple[type(RawConsumptionRecord.time), type(RawConsumptionRecord.value), RawTotalConsumption]
]

ConsumptionTime: TypeAlias = str
ConsumptionValue: TypeAlias = str
ConsumptionForecast: TypeAlias = str
TotalConsumption: TypeAlias = str

RawConsumptionWithRawTotalConsumption = tuple[
    Iterable[RawConsumptionRecord], RawTotalConsumption
]
ConsumptionRow: TypeAlias = tuple[ConsumptionTime, ConsumptionValue]
Consumption: TypeAlias = list[ConsumptionRow]
ConsumptionWithFormattedTimeAndRawValueRow = tuple[ConsumptionTime, RawConsumptionRecord]
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
