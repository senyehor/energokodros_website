from datetime import timedelta
from enum import Enum

# todo
LAST_TIME_AGGREGATION_WAS_RUN_FORMAT = 'TODO'

MAX_AGGREGATION_START_TIME = timedelta(seconds=10)


class AggregationStates(Enum, str):
    IDLE = 'idle'
    RUNNING = 'running'
