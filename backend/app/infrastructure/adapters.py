from app.application.ports import AccessAttempt, AccessEventPublisher, NotificationSender


class LoggingAccessEventPublisher(AccessEventPublisher):
    """Adaptador temporário; será substituído pelo publisher Socket.IO."""

    def publish(self, attempt: AccessAttempt) -> None:
        print(f"access_attempt.created: {attempt}")


class LoggingNotificationSender(NotificationSender):
    """Adaptador temporário; será substituído pelo Firebase Admin SDK."""

    def send_access_alert(self, attempt: AccessAttempt) -> None:
        print(f"access_alert: {attempt}")
