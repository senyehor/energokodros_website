class RunAggregationExceptionBase(Exception):
    ...


class InvalidAggregationState(RunAggregationExceptionBase):
    ...


class AggregationAlreadyRunning(RunAggregationExceptionBase):
    ...


class AggregationDidNotStartWithinMaxStartTime(RunAggregationExceptionBase):
    ...
