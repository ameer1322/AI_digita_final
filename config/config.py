from pydantic import BaseSettings


class Config(BaseSettings):
    SECRET_KEY = "secret boy"  # change this to a long random string
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    MYSQL_USER: str = "user"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DATABASE: str = "main"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    DATABASE_URL: str = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    REDIS_HOST: str =  "localhost"
    REDIS_PORT: int = 6379
    REDIS_TTL: int = 100
