# notifications/services/dispatchers/user_notifications.py
from loguru import logger

from notifications.services.notification_crud_service import NotificationCRUDService


class UserNotificationDispatcher:
    @staticmethod
    def send_status_change_notification(user, old_status, new_status):
        """Sends a notification when a user's status changes (e.g., verified or suspended)."""
        if old_status == new_status:
            return

        if new_status == "verified":
            message = "Your account has been successfully verified! You now have full platform access."
        elif new_status == "suspended":
            message = "Your account has been suspended. Please contact support for assistance."
        else:
            return

        logger.info(
            f"Triggering status change notification for user #{user.id} ({new_status})"
        )

        NotificationCRUDService.create_notification(
            recipient=user, message=message, actor=user, target=user
        )

    @staticmethod
    def send_role_change_notification(user, new_role):
        """Sends a notification when an admin updates a user's role."""
        message = f"Your account role has been updated to: {new_role.capitalize()}."

        logger.info(
            f"Triggering role change notification for user #{user.id} to {new_role}"
        )

        NotificationCRUDService.create_notification(
            recipient=user, message=message, actor=user, target=user
        )
