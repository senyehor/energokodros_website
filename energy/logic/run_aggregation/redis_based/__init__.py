from redis.client import Redis

from energokodros.settings import env
from energy.logic.run_aggregation.config import MAX_AGGREGATION_START_TIME
from energy.logic.run_aggregation.redis_based.aggregation_started_checker import (
    AggregationStartedChecker, AggregationStartedChecker,
)
from energy.logic.run_aggregation.redis_based.runner import (
    RedisAggregationRunner,
    RedisAggregationRunner,
)
from energy.logic.run_aggregation.redis_based.state_retriever import (
    RedisAggregationStateRetriever,
    RedisAggregationStateRetriever,
)

__REDIS = Redis(
    host=env('REDIS_HOST'),
    port=env.int('REDIS_PORT'),
    db=env.int('REDIS_DB'),
    password=env('REDIS_PASSWORD')
)

AGGREGATION_STATE_RETRIEVER = RedisAggregationStateRetriever(
    r=__REDIS,
    state_key=env('AGGREGATION_STATE_KEY'),
    aggregation_last_time_run_key=env('AGGREGATION_LAST_TIME_RUN_KEY')
)

__aggregation_started_checker = AggregationStartedChecker(
    aggregation_start_results_channel=env(
        'AGGREGATION_START_RESULTS_CHANNEL'
    ),
    aggregation_started_successfully_message=env(
        'AGGREGATION_STARTED_SUCCESSFULLY_MESSAGE'
    ),
    aggregation_failed_message=env(
        'AGGREGATION_FAILED_TO_START_MESSAGE'
    ),
    r=__REDIS,
    max_start_time=MAX_AGGREGATION_START_TIME
)

AGGREGATION_RUNNER = RedisAggregationRunner(
    r=__REDIS,
    start_aggregation_message=env('START_AGGREGATION_MESSAGE'),
    start_aggregation_channel=env('AGGREGATOR_CONTROLLER_REDIS_CHANNEL'),
    state_retriever=AGGREGATION_STATE_RETRIEVER,
    aggregation_started_checker=__aggregation_started_checker
)
