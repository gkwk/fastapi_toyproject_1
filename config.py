from pydantic_settings import BaseSettings, SettingsConfigDict

from functools import lru_cache


class Settings(BaseSettings):
    APP_JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def getSettings():
    return Settings()
