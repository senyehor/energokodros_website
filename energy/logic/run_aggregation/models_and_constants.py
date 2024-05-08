from enum import Enum

LAST_TIME_AGGREGATION_WAS_RUN_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class AggregationStates(str, Enum):
    IDLE = 'idle'
    RUNNING = 'running'
