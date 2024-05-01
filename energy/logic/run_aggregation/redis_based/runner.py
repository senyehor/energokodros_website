from redis.client import Redis

from energy.logic.run_aggregation.bases import AggregationRunner
from energy.logic.run_aggregation.exceptions import (
    AggregationAlreadyRunning,
)
from energy.logic.run_aggregation.models_and_constants import AggregationStates
from energy.logic.run_aggregation.redis_based.exceptions import \
    InvalidStartAggregationRequestReceiverCount
from energy.logic.run_aggregation.redis_based.state_retriever import RedisAggregationStateRetriever


class RedisAggregationRunner(AggregationRunner):
    __EXPECTED_START_AGGREGATION_REQUEST_RECEIVER_COUNT = 1

    def __init__(
            self, r: Redis, start_aggregation_message: str,
            aggregator_channel: str, state_retriever: 'RedisAggregationStateRetriever'):
        self.__r = r
        self.__start_aggregation_message = start_aggregation_message
        self.__channel = aggregator_channel
        self.__state_retriever = state_retriever

    def run_aggregation(self):
        state = self.__state_retriever.get_state()
        if state == AggregationStates.RUNNING:
            raise AggregationAlreadyRunning
        self.__send_start_aggregation_message()

    def __send_start_aggregation_message(self):
        receiver_count = self.__r.publish(
            self.__channel,
            self.__start_aggregation_message
        )
        self.__ensure_start_aggregation_message_receiver_count_is_correct(receiver_count)

    def __ensure_start_aggregation_message_receiver_count_is_correct(self, receiver_count: int):
        if receiver_count != self.__EXPECTED_START_AGGREGATION_REQUEST_RECEIVER_COUNT:
            raise InvalidStartAggregationRequestReceiverCount
