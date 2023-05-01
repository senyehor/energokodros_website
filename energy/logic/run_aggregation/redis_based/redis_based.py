from datetime import datetime

from redis.client import Redis

from energy.logic.run_aggregation.bases import AggregationRunner, AggregationStateRetriever
from energy.logic.run_aggregation.exceptions import (
    AggregationAlreadyRunning, AggregationDidNotStartWithinMaxStartTime, InvalidAggregationState,
)
from energy.logic.run_aggregation.models_and_constants import (
    AggregationStates,
    LAST_TIME_AGGREGATION_WAS_RUN_FORMAT, MAX_AGGREGATION_START_TIME,
)
from energy.logic.run_aggregation.redis_based.exceptions import (
    InvalidStartAggregationRequestReceiverCount, ValueWasNotFound,
)


class RedisAggregationRunner(AggregationRunner):
    __EXPECTED_START_AGGREGATION_REQUEST_RECEIVER_COUNT = 1

    def __init__(
            self, r: Redis, start_aggregation_message: str,
            channel: str, state_retriever: 'RedisAggregationStateRetriever'):
        self.__r = r
        self.__start_aggregation_message = start_aggregation_message
        self.__channel = channel
        self.__state_retriever = state_retriever

    def run_aggregation(self):
        state = self.__state_retriever.get_state()
        if state == AggregationStates.RUNNING:
            raise AggregationAlreadyRunning
        self.__send_start_aggregation_message()
        self.__ensure_aggregation_started()

    def __send_start_aggregation_message(self):
        receiver_count = self.__r.publish(
            self.__channel,
            self.__start_aggregation_message
        )
        self.__ensure_start_aggregation_message_receiver_count_is_correct(receiver_count)

    def __ensure_aggregation_started(self):
        now = datetime.now()
        max_aggregation_start_time_past_now = now + MAX_AGGREGATION_START_TIME
        while datetime.now() < max_aggregation_start_time_past_now:
            state = self.__state_retriever.get_state()
            if state != AggregationStates.RUNNING:
                raise AggregationDidNotStartWithinMaxStartTime

    def __ensure_start_aggregation_message_receiver_count_is_correct(self, receiver_count: int):
        if receiver_count != self.__EXPECTED_START_AGGREGATION_REQUEST_RECEIVER_COUNT:
            raise InvalidStartAggregationRequestReceiverCount


class RedisAggregationStateRetriever(AggregationStateRetriever):
    def __init__(self, r: Redis, state_key: str, aggregation_last_time_run_key: str):
        self.__r = r
        self.__state_key = state_key
        self.__aggregation_last_time_run_key = aggregation_last_time_run_key

    def get_state(self) -> AggregationStates:
        raw_state = get_value_from_redis_as_str(
            self.__r,
            self.__state_key
        )
        try:
            return AggregationStates(raw_state)
        except ValueError as e:
            raise InvalidAggregationState from e

    def get_last_time_aggregation_was_run(self) -> datetime | None:
        try:
            raw_last_time_aggregation_was_run = get_value_from_redis_as_str(
                self.__r,
                self.__aggregation_last_time_run_key
            )
        except ValueWasNotFound:
            return None
        return datetime.strptime(
            raw_last_time_aggregation_was_run,
            LAST_TIME_AGGREGATION_WAS_RUN_FORMAT
        )


def get_value_from_redis_as_str(r: Redis, key: str) -> str:
    raw_value = r.get(key)
    if not raw_value:
        raise ValueWasNotFound
    if isinstance(raw_value, bytes):
        raw_value = raw_value.decode()
    return raw_value
