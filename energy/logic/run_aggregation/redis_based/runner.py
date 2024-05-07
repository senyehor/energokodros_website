from datetime import datetime, timedelta

from redis.client import Redis

from energy.logic.run_aggregation.bases import AggregationRunner, AggregationStartedCheckerBase
from energy.logic.run_aggregation.exceptions import AggregationAlreadyRunning
from energy.logic.run_aggregation.models_and_constants import AggregationStates
from energy.logic.run_aggregation.redis_based.exceptions import (
    AggregationStartedConfirmationMessageInvalid, InvalidStartAggregationRequestReceiverCount,
)
from energy.logic.run_aggregation.redis_based.state_retriever import RedisAggregationStateRetriever


class RedisAggregationRunner(AggregationRunner):
    __EXPECTED_START_AGGREGATION_REQUEST_RECEIVER_COUNT = 1

    def __init__(
            self, r: Redis, start_aggregation_message: str,
            start_aggregation_channel: str, state_retriever: RedisAggregationStateRetriever,
            aggregation_started_checker: 'AggregationStartedChecker'
    ):
        self.__r = r
        self.__start_aggregation_message = start_aggregation_message
        self.__channel = start_aggregation_channel
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
            raise InvalidStartAggregationRequestReceiverCount(receiver_count)


class AggregationStartedChecker(AggregationStartedCheckerBase):
    def __init__(
            self, aggregation_started_confirmation_channel: str,
            aggregation_started_confirmation_message: str, r: Redis,
            max_start_time: timedelta
    ):
        self.__channel = r.pubsub()
        self.__channel.subscribe(aggregation_started_confirmation_channel)
        self.__confirmation_message = aggregation_started_confirmation_message
        self.__max_start_time = max_start_time

    def check_aggregation_started(self) -> bool:
        max_wait_time = datetime.now() + self.__max_start_time
        while datetime.now() < max_wait_time:
            if self.__try_get_aggregation_started_message():
                return True
        return False

    def __try_get_aggregation_started_message(self):
        if message := self.__channel.get_message():
            data = message.get('data').decode()
            if data == self.__confirmation_message:
                return True
            raise AggregationStartedConfirmationMessageInvalid
        return False
