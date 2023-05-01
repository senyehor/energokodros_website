from redis.client import Redis

from energy.logic.run_aggregation.redis_based.exceptions import (
    ValueWasNotFound,
)


def get_value_from_redis_as_str(r: Redis, key: str) -> str:
    raw_value = r.get(key)
    if not raw_value:
        raise ValueWasNotFound
    if isinstance(raw_value, bytes):
        raw_value = raw_value.decode()
    return raw_value
