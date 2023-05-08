from datetime import datetime, timedelta

from redis.client import Redis

from energy.logic.run_aggregation.bases import AggregationStartedCheckerBase
from energy.logic.run_aggregation.redis_based.exceptions import \
    AggregationStartedConfirmationMessageInvalid


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
