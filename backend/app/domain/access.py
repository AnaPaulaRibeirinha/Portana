from dataclasses import dataclass
from datetime import datetime, time
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    PORTEIRO = "porteiro"
    MORADOR = "morador"
    VISITANTE = "visitante"


class AccessDecision(StrEnum):
    ALLOWED = "allowed"
    USER_INACTIVE = "user_inactive"
    OUTSIDE_SCHEDULE = "outside_schedule"
    ACCESS_POINT_NOT_ALLOWED = "access_point_not_allowed"


@dataclass(frozen=True)
class AccessRule:
    weekdays: frozenset[int]
    start_time: time
    end_time: time
    access_points: frozenset[str]

    def allows(self, at: datetime, access_point: str) -> bool:
        if at.weekday() not in self.weekdays:
            return False
        if access_point not in self.access_points:
            return False
        return self.start_time <= at.time() <= self.end_time


@dataclass(frozen=True)
class AccessSubject:
    user_id: str
    active: bool
    rule: AccessRule | None


def decide_access(subject: AccessSubject, access_point: str, at: datetime) -> AccessDecision:
    if not subject.active:
        return AccessDecision.USER_INACTIVE
    if subject.rule is None:
        return AccessDecision.OUTSIDE_SCHEDULE
    if subject.rule.allows(at, access_point):
        return AccessDecision.ALLOWED
    if access_point not in subject.rule.access_points:
        return AccessDecision.ACCESS_POINT_NOT_ALLOWED
    return AccessDecision.OUTSIDE_SCHEDULE
