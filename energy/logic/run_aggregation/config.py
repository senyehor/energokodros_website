from datetime import timedelta

from energokodros.settings import env

MAX_AGGREGATION_START_TIME = timedelta(
    seconds=env.int('MAX_AGGREGATION_START_TIME_SECONDS')
)
