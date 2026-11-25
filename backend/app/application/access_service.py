from datetime import datetime

from app.application.ports import (
    AccessAttempt,
    AccessAttemptRepository,
    AccessEventPublisher,
    NotificationSender,
    SubjectRepository,
)
from app.domain.access import AccessDecision, decide_access


class AccessService:
    def __init__(
        self,
        subjects: SubjectRepository,
        attempts: AccessAttemptRepository,
        events: AccessEventPublisher,
        notifications: NotificationSender,
    ) -> None:
        self._subjects = subjects
        self._attempts = attempts
        self._events = events
        self._notifications = notifications

    def simulate(self, user_id: str, access_point: str, at: datetime) -> AccessAttempt:
        subject = self._subjects.get_subject(user_id)
        decision = (
            AccessDecision.USER_INACTIVE
            if subject is None
            else decide_access(subject, access_point, at)
        )
        attempt = AccessAttempt(user_id, access_point, at, decision)
        saved = self._attempts.save(attempt)
        self._events.publish(saved)
        if saved.decision is not AccessDecision.ALLOWED:
            self._notifications.send_access_alert(saved)
        return saved
