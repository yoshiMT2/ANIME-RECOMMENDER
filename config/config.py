from __future__ import annotations

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    openai_api_key: SecretStr = Field(alias='OPENAI_API_KEY')

    model_name: str = Field(default='gpt-5-mini', alias='MODEL_NAME')
    env: str = Field(default='dev', alias='ENV')


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
