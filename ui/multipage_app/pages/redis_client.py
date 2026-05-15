import redis

from redis_config import redis_config



redis_client = redis.Redis(
    host = redis_config.REDIS_HOST,
    port = redis_config.REDIS_PORT,
    decode_responses=True
)
