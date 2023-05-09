from datetime import datetime, timedelta

from redis.client import Redis

from energy.logic.run_aggregation.bases import AggregationStartedCheckerBase
from energy.logic.run_aggregation.redis_based.exceptions import (
    AggregationStartedConfirmationMessageInvalid, SubOrUnsubMessageTypeExpected,
)


class AggregationStartedChecker(AggregationStartedCheckerBase):
    def __init__(
            self, aggregation_start_results_channel: str,
            aggregation_started_successfully_message: str,
            aggregation_failed_message: str,
            r: Redis, max_start_time: timedelta
    ):
        self.__pubsub = r.pubsub()
        self.__aggregation_start_results_channel = aggregation_start_results_channel
        self.__confirmation_message = aggregation_started_successfully_message
        self.__failure_message = aggregation_failed_message
        self.__max_start_time = max_start_time

    def check_aggregation_started(self) -> bool:
        # sub and unsub each time, as otherwise there are too many subscribers,
        # probably due to how gunicorn pre-forks
        self.__subscribe_to_channel()
        aggregation_started = self.__check_aggregation_started()
        self.__unsubscribe_from_channel()
        return aggregation_started

    def __check_aggregation_started(self):
        max_wait_time = datetime.now() + self.__max_start_time
        while datetime.now() < max_wait_time:
            if self.__get_aggregation_started():
                return True
        return False

    def __get_aggregation_started(self) -> bool:
        if message := self.__pubsub.get_message():
            data = message.get('data').decode()
            if data == self.__confirmation_message:
                return True
            if data == self.__failure_message:
                return False
            raise AggregationStartedConfirmationMessageInvalid
        return False

    def __subscribe_to_channel(self):
        self.__pubsub.subscribe(self.__aggregation_start_results_channel)
        self.__dump_message()

    def __unsubscribe_from_channel(self):
        self.__pubsub.unsubscribe(self.__aggregation_start_results_channel)
        self.__dump_message()

    def __dump_message(self):
        # timeout needed as sometimes program is too fast
        # and message is created after we try to dump it, so it clutters channel
        message = self.__pubsub.get_message(timeout=1)
        if message.get('type') not in ('subscribe', 'unsubscribe'):
            raise SubOrUnsubMessageTypeExpected
