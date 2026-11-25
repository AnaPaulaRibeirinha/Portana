from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

from app.domain.access import AccessDecision, AccessSubject


@dataclass(frozen=True)
class AccessAttempt:
    user_id: str
    access_point: str
    occurred_at: datetime
    decision: AccessDecision


class SubjectRepository(Protocol):
    def get_subject(self, user_id: str) -> AccessSubject | None: ...


class AccessAttemptRepository(Protocol):
    def save(self, attempt: AccessAttempt) -> AccessAttempt: ...


class AccessEventPublisher(Protocol):
    def publish(self, attempt: AccessAttempt) -> None: ...


class NotificationSender(Protocol):
    def send_access_alert(self, attempt: AccessAttempt) -> None: ...
