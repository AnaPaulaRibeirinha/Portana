from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Portana API"
    environment: str = "development"
    database_url: str = "sqlite:///./portana.db"
    jwt_secret_key: str = "change-me-in-development"
    fcm_enabled: bool = False

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
