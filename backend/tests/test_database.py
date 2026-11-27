from datetime import datetime, time

from sqlalchemy.orm import Session, sessionmaker

from app.application.ports import AccessAttempt
from app.domain.access import AccessDecision
from app.infrastructure.database import Base, create_database_engine, init_db
from app.infrastructure.models import AccessRuleModel, UserModel
from app.infrastructure.repositories import (
    SqlAlchemyAccessAttemptRepository,
    SqlAlchemySubjectRepository,
)


def test_sqlalchemy_repositories_round_trip() -> None:
    engine = create_database_engine("sqlite+pysqlite:///:memory:")
    init_db(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

    with SessionLocal() as session:
        session.add(
            UserModel(
                id="u-1",
                name="Maria",
                email="maria@example.com",
                password_hash="hash",
                role="morador",
                active=True,
                access_rule=AccessRuleModel(
                    weekdays=[0],
                    start_time=time(8),
                    end_time=time(18),
                    access_points=["main"],
                ),
            )
        )
        session.commit()

        subject = SqlAlchemySubjectRepository(session).get_subject("u-1")
        assert subject is not None
        assert subject.rule is not None
        assert subject.rule.allows(datetime(2026, 11, 23, 10), "main")

        attempt = AccessAttempt("u-1", "main", datetime(2026, 11, 23, 10), AccessDecision.ALLOWED)
        SqlAlchemyAccessAttemptRepository(session).save(attempt)
        assert session.query(Base.metadata.tables["access_attempts"]).count() == 1

    engine.dispose()
