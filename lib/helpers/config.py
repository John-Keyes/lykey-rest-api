from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

@lru_cache
def GetSettings():
    return Settings()


class Settings(BaseSettings):
    MODE: str
    DB_HOST: str
    DB_USER: str
    DB_PWD: str
    DB_ROOT_PWD: str
    DB_PORT: int
    EXTRA_DB_PORT: int
    DB_NAME: str
    DB_URL:  str = ""

    API_PORT: int
    CLIENT_PORT: int
    CLIENT_URL: str
    API_URL: str
    ALGORITHM: str

    TOKEN_KEY: str
    REDIS_URL: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    BUCKET_NAME: str

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str

    model_config = SettingsConfigDict(env_file=".env")