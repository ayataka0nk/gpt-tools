from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    openai_api_key: str = "OPENAI_API_KEY"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
