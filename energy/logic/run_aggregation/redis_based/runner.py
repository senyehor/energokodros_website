from redis.client import Redis

from energy.logic.run_aggregation.bases import AggregationRunnerBase
from energy.logic.run_aggregation.exceptions import (
    AggregationAlreadyRunning,
    AggregationDidNotStart,
)
from energy.logic.run_aggregation.models_and_constants import AggregationStates
from energy.logic.run_aggregation.redis_based.aggregation_started_checker import \
    AggregationStartedChecker
from energy.logic.run_aggregation.redis_based.exceptions import (
    InvalidStartAggregationRequestReceiverCount,
)
from energy.logic.run_aggregation.redis_based.state_retriever import RedisAggregationStateRetriever


class RedisAggregationRunner(AggregationRunnerBase):
    __EXPECTED_START_AGGREGATION_REQUEST_RECEIVER_COUNT = 1

    def __init__(
            self, r: Redis, start_aggregation_message: str,
            start_aggregation_channel: str, state_retriever: RedisAggregationStateRetriever,
            aggregation_started_checker: AggregationStartedChecker
    ):
        self.__r = r
        self.__start_aggregation_message = start_aggregation_message
        self.__channel = start_aggregation_channel
        self.__state_retriever = state_retriever
        self.__aggregation_started_checker = aggregation_started_checker

    def run_aggregation(self):
        self.__ensure_aggregation_is_not_running()
        self.__send_start_aggregation_message()
        self.__ensure_aggregation_started()

    def __ensure_aggregation_started(self):
        if self.__aggregation_started_checker.check_aggregation_started():
            return
        raise AggregationDidNotStart

    def __send_start_aggregation_message(self):
        receiver_count = self.__r.publish(
            self.__channel,
            self.__start_aggregation_message
        )
        self.__ensure_start_aggregation_message_receiver_count_is_correct(receiver_count)

    def __ensure_aggregation_is_not_running(self):
        state = self.__state_retriever.get_state()
        if state == AggregationStates.RUNNING:
            raise AggregationAlreadyRunning

    def __ensure_start_aggregation_message_receiver_count_is_correct(self, receiver_count: int):
        if receiver_count != self.__EXPECTED_START_AGGREGATION_REQUEST_RECEIVER_COUNT:
            raise InvalidStartAggregationRequestReceiverCount(receiver_count)
