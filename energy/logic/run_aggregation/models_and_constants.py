from enum import Enum

# todo
LAST_TIME_AGGREGATION_WAS_RUN_FORMAT = 'TODO'


class AggregationStates(str, Enum):
    IDLE = 'idle'
    RUNNING = 'running'
