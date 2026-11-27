from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()


def create_database_engine(database_url: str) -> Engine:
    """Cria o engine com opções específicas para SQLite e PostgreSQL."""
    is_sqlite = database_url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    engine_options: dict[str, object] = {
        "connect_args": connect_args,
        "pool_pre_ping": True,
    }
    if not is_sqlite:
        engine_options.update(pool_size=10, max_overflow=20)
    # Um banco SQLite em memória precisa de uma conexão única para que as
    # tabelas continuem disponíveis entre sessões, especialmente nos testes.
    if database_url.endswith(":memory:"):
        engine_options["poolclass"] = StaticPool
    return create_engine(database_url, **engine_options)


engine = create_database_engine(settings.database_url)
SessionLocal = sessionmaker[Session](bind=engine, autoflush=False, expire_on_commit=False)


def init_db(database_engine: Engine = engine) -> None:
    from app.infrastructure import models  # noqa: F401

    Base.metadata.create_all(bind=database_engine)


def get_db() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
