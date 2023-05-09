from datetime import datetime

from redis.client import Redis

from energy.logic.run_aggregation.bases import AggregationStateRetrieverBase
from energy.logic.run_aggregation.exceptions import InvalidAggregatorState
from energy.logic.run_aggregation.models_and_constants import (
    AggregationStates,
    LAST_TIME_AGGREGATION_WAS_RUN_FORMAT,
)
from energy.logic.run_aggregation.redis_based.exceptions import ValueWasNotFound
from energy.logic.run_aggregation.redis_based.utils import get_value_from_redis_as_str


class RedisAggregationStateRetriever(AggregationStateRetrieverBase):
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
            raise InvalidAggregatorState from e

    def get_last_time_aggregation_was_run(self, formatted=False) -> datetime | str | None:
        try:
            raw_last_time_aggregation_was_run = get_value_from_redis_as_str(
                self.__r,
                self.__aggregation_last_time_run_key
            )
        except ValueWasNotFound:
            return None
        last_time_run = datetime.strptime(
            raw_last_time_aggregation_was_run,
            LAST_TIME_AGGREGATION_WAS_RUN_FORMAT
        )
        if formatted:
            return last_time_run.strftime('%H:%M %d-%m-%Y')
        return last_time_run
