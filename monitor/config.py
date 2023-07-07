from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    meilisearch_url: str = "http://localhost:7700"
    meilisearch_api_key: str = "masterKey"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()
