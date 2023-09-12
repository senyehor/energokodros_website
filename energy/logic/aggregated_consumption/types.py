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


Consumption: TypeAlias = Iterable[ConsumptionRecord]


class ConsumptionRecordRawAndFormatted(NamedTuple):
    raw_consumption_record: RawConsumptionRecord
    formatted_consumption_record: ConsumptionRecord


ConsumptionRawAndFormatted = Iterable[ConsumptionRecordRawAndFormatted]

RawConsumptionWithRawTotalConsumption = tuple[
    Iterable[RawConsumptionRecord], RawTotalConsumption
]


class ConsumptionRecordWithForecastForIt(NamedTuple):
    # ConsumptionRecord is not the parent to make field order more explicit
    time: ConsumptionTime
    value: ConsumptionValue
    forecast: ConsumptionForecast


class ConsumptionForecastRawAndFormatted(NamedTuple):
    raw: RawConsumptionForecast
    formatted: ConsumptionForecast


class ConsumptionRecordRawAndFormattedWithRawAndFormattedForecast(NamedTuple):
    raw_consumption_record: RawConsumptionRecord
    formatted_consumption_record: ConsumptionRecord
    forecast_raw_and_formatted: ConsumptionForecastRawAndFormatted


ConsumptionWithConsumptionForecast = Iterable[ConsumptionRecordWithForecastForIt]
ConsumptionRawAndFormattedWithForecastRawAndFormatted = Iterable[
    ConsumptionRecordRawAndFormattedWithRawAndFormattedForecast
]

HOUR: TypeAlias = int
