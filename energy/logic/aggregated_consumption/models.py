from datetime import timedelta
from enum import IntEnum


class AggregationIntervalSeconds(IntEnum):
    ONE_HOUR = int(timedelta(hours=1).total_seconds())
    ONE_DAY = int(timedelta(days=1).total_seconds())
    ONE_WEEK = int(timedelta(weeks=1).total_seconds())
    ONE_MONTH = int(timedelta(weeks=4).total_seconds())
    ONE_YEAR = int(timedelta(weeks=4 * 12).total_seconds())
