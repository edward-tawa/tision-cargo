from django.db import transaction
from loguru import logger
from rest_framework.exceptions import PermissionDenied, ValidationError

from notifications.services.notification_crud_service import NotificationCRUDService


class NotificationBusinessService:
    """
    Business logic service class for handling complex operations
    related to notifications, state management, ownership validation,
    and real-time distribution hooks.
    """

    @staticmethod
    @transaction.atomic
    def send_notification_to_user(
        *,
        recipient,
        message,
        actor=None,
        target=None,
    ):
        """
        Business logic wrapper to dispatch a notification to a user.
        Enforces domain rules and coordinates creation via the CRUD service.
        """
        recipient_id = recipient.id if hasattr(recipient, "id") else recipient
        logger.info(f"Attempting to send notification to recipient #{recipient_id}")

        if not recipient:
            logger.error("Notification dispatch failed: Recipient is missing.")
            raise ValidationError(
                {"detail": "A notification recipient must be specified."}
            )

        # Create notification via CRUD service
        notification = NotificationCRUDService.create_notification(
            recipient=recipient,
            message=message,
            actor=actor,
            target=target,
        )

        logger.success(
            f"Notification #{notification.id} successfully dispatched to recipient #{recipient_id}."
        )
        return notification

    @staticmethod
    @transaction.atomic
    def mark_notification_as_read(*, notification_id, user):
        """
        Allows a user to mark a specific notification as read,
        enforcing security and ownership validation.
        """
        logger.info(
            f"User #{user.id} attempting to mark Notification #{notification_id} as read."
        )

        notification = NotificationCRUDService.get_notification(notification_id)

        # 1. Permission guard: Only the recipient can mark their own notification as read
        if notification.recipient != user:
            logger.warning(
                f"Unauthorized mark-as-read attempt by User #{user.id} on Notification #{notification_id}"
            )
            raise PermissionDenied(
                "You do not have permission to modify this notification."
            )

        # 2. State validation: Avoid redundant writes if already read
        if notification.is_read:
            logger.info(f"Notification #{notification_id} is already marked as read.")
            return notification

        # Update via CRUD service
        updated_notification = NotificationCRUDService.update_notification(
            notification_id=notification.id,
            is_read=True,
        )

        logger.success(
            f"Notification #{notification.id} marked as read by User #{user.id}."
        )
        return updated_notification

    @staticmethod
    @transaction.atomic
    def mark_all_user_notifications_as_read(*, user):
        """
        Marks all unread notifications for a given user as read in bulk.
        """
        logger.info(f"User #{user.id} attempting to mark all notifications as read.")

        if not user.is_authenticated:
            raise PermissionDenied("Authentication is required.")

        updated_count = NotificationCRUDService.mark_all_as_read(recipient=user)

        logger.success(
            f"Successfully marked {updated_count} notifications as read for User #{user.id}."
        )
        return updated_count

    @staticmethod
    @transaction.atomic
    def delete_user_notification(*, notification_id, user):
        """
        Allows a user to delete one of their notifications with ownership validation.
        """
        logger.warning(
            f"User #{user.id} attempting to delete Notification #{notification_id}"
        )

        notification = NotificationCRUDService.get_notification(notification_id)

        if notification.recipient != user:
            logger.warning(
                f"Unauthorized deletion attempt by User #{user.id} on Notification #{notification_id}"
            )
            raise PermissionDenied(
                "You do not have permission to delete this notification."
            )

        NotificationCRUDService.delete_notification(notification_id)

        logger.success(
            f"Notification #{notification_id} deleted successfully by User #{user.id}."
        )
        return True
