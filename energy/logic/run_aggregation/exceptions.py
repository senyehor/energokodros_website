class RunAggregationExceptionBase(Exception):
    ...


class InvalidAggregatorState(RunAggregationExceptionBase):
    ...


class AggregationAlreadyRunning(RunAggregationExceptionBase):
    ...


class AggregationDidNotStart(RunAggregationExceptionBase):
    ...
