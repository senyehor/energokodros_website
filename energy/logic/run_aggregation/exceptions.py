class RunAggregationExceptionBase(Exception):
    ...


class InvalidAggregatorState(RunAggregationExceptionBase):
    ...


class AggregationAlreadyRunning(RunAggregationExceptionBase):
    ...
