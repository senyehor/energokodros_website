from energy.logic.run_aggregation.exceptions import RunAggregationExceptionBase


class InvalidStartAggregationRequestReceiverCount(RunAggregationExceptionBase):
    def __init__(self, actual_receiver_count: int):
        self.__actual_receiver_count = actual_receiver_count

    def __str__(self):
        return f'{super().__str__()}\n' \
               f'actual receiver count: {self.__actual_receiver_count}'


class ValueWasNotFound(RunAggregationExceptionBase):
    ...
