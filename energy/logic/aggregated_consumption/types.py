from datetime import datetime
from decimal import Decimal
from typing import Iterable, NamedTuple, TypeAlias

RawConsumptionValue: TypeAlias = Decimal
RawConsumptionTime: TypeAlias = datetime | str
RawConsumptionForecast: TypeAlias = float
RawTotalConsumption: TypeAlias = Decimal


class RawConsumptionRecord(NamedTuple):
    time: RawConsumptionTime
    value: RawConsumptionValue


RawConsumption = Iterable[RawConsumptionRecord]

RawQueryRows = Iterable[
    tuple[type(RawConsumptionRecord.time), type(RawConsumptionRecord.value), RawTotalConsumption]
]

ConsumptionTime: TypeAlias = str
ConsumptionValue: TypeAlias = str
ConsumptionForecast: TypeAlias = str
TotalConsumption: TypeAlias = str


class ConsumptionRecord(NamedTuple):
    time: ConsumptionTime
    value: ConsumptionValue


class ConsumptionRecordRawAndFormatted(NamedTuple):
    raw: RawConsumptionRecord
    formatted: ConsumptionRecord


ConsumptionRawAndFormatted = Iterable[ConsumptionRecordRawAndFormatted]

Consumption: TypeAlias = Iterable[ConsumptionRecord]

RawConsumptionWithRawTotalConsumption = tuple[
    Iterable[RawConsumptionRecord], RawTotalConsumption
]

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
