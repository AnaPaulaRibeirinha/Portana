from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.ports import AccessAttempt, AccessAttemptRepository, SubjectRepository
from app.domain.access import AccessRule, AccessSubject
from app.infrastructure.models import AccessAttemptModel, UserModel


class SqlAlchemySubjectRepository(SubjectRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_subject(self, user_id: str) -> AccessSubject | None:
        user = self._session.scalar(select(UserModel).where(UserModel.id == user_id))
        if user is None:
            return None
        rule = user.access_rule
        domain_rule = None
        if rule is not None:
            domain_rule = AccessRule(
                weekdays=frozenset(rule.weekdays),
                start_time=rule.start_time,
                end_time=rule.end_time,
                access_points=frozenset(rule.access_points),
            )
        return AccessSubject(user_id=user.id, active=user.active, rule=domain_rule)


class SqlAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_email(self, email: str) -> UserModel | None:
        return self._session.scalar(select(UserModel).where(UserModel.email == email.lower()))

    def get_by_id(self, user_id: str) -> UserModel | None:
        return self._session.get(UserModel, user_id)


class SqlAlchemyAccessAttemptRepository(AccessAttemptRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, attempt: AccessAttempt) -> AccessAttempt:
        record = AccessAttemptModel(
            user_id=attempt.user_id,
            access_point=attempt.access_point,
            occurred_at=attempt.occurred_at,
            decision=attempt.decision.value,
        )
        self._session.add(record)
        self._session.commit()
        return attempt
