from _decimal import Decimal
from datetime import datetime

from typing_extensions import TypeAlias

ConsumptionForecast: TypeAlias = float
ConsumptionTime: TypeAlias = datetime | str
ConsumptionValue: TypeAlias = Decimal

FormattedConsumptionTime: TypeAlias = str
FormattedConsumptionValue: TypeAlias = str
FormattedConsumptionForecast: TypeAlias = str

RawAggregatedConsumptionData = list[tuple[ConsumptionTime, ConsumptionValue]] | None
AggregatedConsumptionData: TypeAlias = \
    list[
        tuple[FormattedConsumptionTime, FormattedConsumptionValue, FormattedConsumptionForecast]
    ] | None
RawAggregatedConsumptionDataWithForecast: TypeAlias = \
    list[tuple[ConsumptionTime, ConsumptionValue, ConsumptionForecast]]

HOUR: TypeAlias = int
