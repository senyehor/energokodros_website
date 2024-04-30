from redis.client import Redis

from energokodros.settings import env
from energy.logic.run_aggregation.redis_based.runner import RedisAggregationRunner
from energy.logic.run_aggregation.redis_based.state_retriever import RedisAggregationStateRetriever

REDIS = Redis(
    host=env('REDIS_HOST'),
    port=env.int('REDIS_PORT'),
    db=env.int('REDIS_DB'),
    password=env('REDIS_PASSWORD')
)

AGGREGATION_STATE_RETRIEVER = RedisAggregationStateRetriever(
    r=REDIS,
    state_key=env('AGGREGATION_STATE_KEY'),
    aggregation_last_time_run_key=env('AGGREGATION_LAST_TIME_RUN_KEY')
)

AGGREGATION_RUNNER = RedisAggregationRunner(
    r=REDIS,
    start_aggregation_message=env('START_AGGREGATION_MESSAGE'),
    aggregator_channel=env('AGGREGATOR_REDIS_CHANNEL'),
    state_retriever=AGGREGATION_STATE_RETRIEVER
)
