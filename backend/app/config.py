from functools import lru_cache

from typing import Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "testing", "staging", "production"]


class Settings(BaseSettings):
    app_name: str = "Portana API"
    environment: Environment = "development"
    database_url: str = "postgresql+psycopg://portana:portana@localhost:5432/portana"
    jwt_secret_key: str = "change-me-in-development"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=60, gt=0)
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    socketio_enabled: bool = True
    socketio_path: str = "/socket.io"
    fcm_enabled: bool = False
    fcm_credentials_path: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("DATABASE_URL não pode ser vazio")
        normalized = value.strip()
        if normalized.startswith("postgres://"):
            return "postgresql+psycopg://" + normalized.removeprefix("postgres://")
        if normalized.startswith("postgresql://"):
            return "postgresql+psycopg://" + normalized.removeprefix("postgresql://")
        if normalized.startswith(("postgresql+psycopg://", "sqlite://", "sqlite+")):
            return normalized
        raise ValueError("DATABASE_URL deve usar PostgreSQL ou SQLite")

    @model_validator(mode="after")
    def validate_production_security(self) -> "Settings":
        if self.environment == "production" and len(self.jwt_secret_key) < 32:
            raise ValueError("JWT_SECRET_KEY de produção deve ter pelo menos 32 caracteres")
        return self

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
