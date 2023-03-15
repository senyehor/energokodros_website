from _decimal import Decimal
from datetime import datetime

from typing import TypeAlias

RawConsumptionForecast: TypeAlias = float
RawConsumptionTime: TypeAlias = datetime | str
RawConsumptionValue: TypeAlias = Decimal
RawTotalConsumption: TypeAlias = Decimal

ConsumptionTime: TypeAlias = str
ConsumptionValue: TypeAlias = str
ConsumptionForecast: TypeAlias = str
TotalConsumption: TypeAlias = str

RawConsumptionData = list[tuple[RawConsumptionTime, RawConsumptionValue]]
RawConsumptionDataWIthRawTotalConsumption = tuple[
    RawConsumptionData, RawTotalConsumption
]
Consumption: TypeAlias = \
    list[
        tuple[ConsumptionTime, ConsumptionValue]
    ]
ConsumptionWithConsumptionForecast: TypeAlias = \
    list[tuple[ConsumptionTime, ConsumptionValue, ConsumptionForecast]]
ConsumptionWithTotalConsumption = tuple[
    Consumption, TotalConsumption
]
ConsumptionWIthConsumptionForecastWithTotalConsumption = tuple[
    ConsumptionWithConsumptionForecast, TotalConsumption
]

HOUR: TypeAlias = int
