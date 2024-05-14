from enum import Enum

LAST_TIME_AGGREGATION_WAS_RUN_FORMAT = '%Y-%m-%d %H:%M:%S %z'


class AggregationStates(str, Enum):
    IDLE = 'idle'
    RUNNING = 'running'
