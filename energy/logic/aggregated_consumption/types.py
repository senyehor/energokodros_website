from _decimal import Decimal
from datetime import datetime

from typing import TypeAlias

RawConsumptionForecast: TypeAlias = float
RawConsumptionTime: TypeAlias = datetime | str
RawConsumptionValue: TypeAlias = Decimal
RawTotalConsumption: TypeAlias = Decimal

FormattedConsumptionTime: TypeAlias = str
FormattedConsumptionValue: TypeAlias = str
FormattedConsumptionForecast: TypeAlias = str
FormattedTotalConsumption: TypeAlias = str

RawAggregatedConsumptionData = list[tuple[RawConsumptionTime, RawConsumptionValue]]
RawAggregatedConsumptionDataWithRawTotalConsumption = tuple[
    RawAggregatedConsumptionData, RawTotalConsumption
]
AggregatedConsumptionData: TypeAlias = \
    list[
        tuple[FormattedConsumptionTime, FormattedConsumptionValue]
    ]
AggregatedConsumptionDataWithForecast: TypeAlias = \
    list[tuple[FormattedConsumptionTime, FormattedConsumptionValue, FormattedConsumptionForecast]]
AggregatedConsumptionDataWithTotalConsumption = tuple[
    AggregatedConsumptionData, FormattedTotalConsumption
]

HOUR: TypeAlias = int
