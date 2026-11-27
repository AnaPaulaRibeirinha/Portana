import pytest
from pydantic import ValidationError

from app.config import Settings


def test_normalizes_postgres_url_without_driver() -> None:
    settings = Settings(database_url="postgresql://user:pass@localhost/portana")

    assert settings.database_url == "postgresql+psycopg://user:pass@localhost/portana"
    assert not settings.is_production


def test_accepts_sqlite_for_isolated_tests() -> None:
    settings = Settings(database_url="sqlite+pysqlite:///:memory:", environment="testing")

    assert settings.database_url.startswith("sqlite+")


def test_exposes_realtime_and_push_settings() -> None:
    settings = Settings(socketio_enabled=True, fcm_enabled=True, fcm_credentials_path="/tmp/fcm.json")

    assert settings.socketio_path == "/socket.io"
    assert settings.fcm_credentials_path == "/tmp/fcm.json"


def test_rejects_weak_production_secret() -> None:
    with pytest.raises(ValidationError, match="32 caracteres"):
        Settings(environment="production", jwt_secret_key="short-secret")
