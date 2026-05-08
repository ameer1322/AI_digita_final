from pydantic import BaseSettings


class RedisConfig(BaseSettings):
    REDIS_HOST: str =  "localhost"
    REDIS_PORT: int = 6379
    REDIS_TTL: int = 100


redis_config = RedisConfig()