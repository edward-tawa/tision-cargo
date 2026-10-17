from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class Notification(TimeStampModel):
    """Represents a notification for a user."""

    # 1. RECIPIENT (Always a human user)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    # 2. ACTOR (Generic: Can be a User, Truck, Booking, etc.)
    actor_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="actor_notifications",
    )
    actor_object_id = models.PositiveIntegerField(null=True, blank=True)
    actor = GenericForeignKey("actor_content_type", "actor_object_id")

    # 3. TARGET (Generic: Can be a Bid, Shipment, Invoice, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,  # Made optional in case some notifications don't have a target
        related_name="target_notifications",
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target_object = GenericForeignKey(
        "target_content_type", "target_object_id"
    )  # <-- Fixed names!

    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "created_at"]),
            models.Index(fields=["recipient", "is_read"]),
        ]

    def __str__(self):
        return f"Notification {self.id} for User {self.recipient_id}"
