from datetime import datetime, time

from app.domain.access import AccessDecision, AccessRule, AccessSubject, decide_access


def test_allows_access_inside_rule() -> None:
    subject = AccessSubject(
        user_id="u-1",
        active=True,
        rule=AccessRule(frozenset({0}), time(8), time(18), frozenset({"main"})),
    )

    assert decide_access(subject, "main", datetime(2026, 11, 23, 10)) is AccessDecision.ALLOWED


def test_denies_access_outside_schedule() -> None:
    subject = AccessSubject(
        user_id="u-1",
        active=True,
        rule=AccessRule(frozenset({0}), time(8), time(18), frozenset({"main"})),
    )

    assert decide_access(subject, "main", datetime(2026, 11, 23, 19)) is AccessDecision.OUTSIDE_SCHEDULE
