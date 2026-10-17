from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from loguru import logger
from rest_framework.exceptions import ValidationError

from notifications.models.notification_model import (
    Notification,
)


class NotificationCRUDService:
    """
    CRUD service class for handling database operations related to Notification objects
    using loguru logging and explicit keyword-only arguments.
    """

    @staticmethod
    def get_notification(notification_id):
        """Retrieve a single notification by its ID."""
        logger.info(f"Fetching Notification #{notification_id}")
        try:
            return Notification.objects.get(id=notification_id)
        except Notification.DoesNotExist:
            logger.error(f"Notification #{notification_id} not found.")
            raise ValidationError(
                {"detail": f"Notification #{notification_id} does not exist."}
            )

    @staticmethod
    def get_notifications(recipient=None, is_read=None):
        """Retrieve a filtered list of notifications."""
        logger.info(
            "Fetching notifications list with filters: recipient=%s, is_read=%s",
            recipient,
            is_read,
        )
        queryset = Notification.objects.all()

        if recipient:
            queryset = queryset.filter(recipient_id=recipient)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)

        return queryset.order_by("-created_at")

    @staticmethod
    @transaction.atomic
    def create_notification(*, recipient, message, actor=None, target=None):
        """
        Create a new notification record with optional generic actor and target.
        """
        logger.info(f"Creating new notification for recipient #{recipient}")

        notification = Notification(recipient=recipient, message=message)

        # Attach generic actor if provided (e.g., a Truck, a Booking, or a User)
        if actor:
            notification.actor_content_type = ContentType.objects.get_for_model(actor)
            notification.actor_object_id = actor.pk

        # Attach generic target if provided (e.g., a Shipment, an Invoice)
        if target:
            notification.target_content_type = ContentType.objects.get_for_model(target)
            notification.target_object_id = target.pk

        notification.save()
        logger.success(f"Notification #{notification.id} successfully created.")
        return notification

    @staticmethod
    @transaction.atomic
    def update_notification(notification_id, *, is_read=None, message=None):
        """Update an existing notification's details."""
        logger.info(f"Updating Notification #{notification_id}")
        notification = NotificationCRUDService.get_notification(notification_id)

        if is_read is not None:
            notification.is_read = is_read
        if message is not None:
            notification.message = message

        notification.save()
        logger.success(f"Notification #{notification.id} successfully updated.")
        return notification

    @staticmethod
    @transaction.atomic
    def mark_all_as_read(recipient):
        """Mark all unread notifications for a specific recipient as read."""
        logger.info(f"Marking all notifications as read for recipient #{recipient}")
        updated_count = Notification.objects.filter(
            recipient_id=recipient, is_read=False
        ).update(is_read=True)
        logger.success(
            f"Marked {updated_count} notifications as read for recipient #{recipient}."
        )
        return updated_count

    @staticmethod
    @transaction.atomic
    def delete_notification(notification_id):
        """Delete a notification record."""
        logger.warning(f"Deleting Notification #{notification_id}")
        notification = NotificationCRUDService.get_notification(notification_id)
        notification.delete()
        logger.success(f"Notification #{notification.id} deleted successfully.")
        return True
