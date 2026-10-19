import uuid

from django.conf import settings
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class ChatThread(TimeStampModel):
    """
    Represents a specific chat room/container for a single transaction between
    a client and a driver.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Linked directly to the booking/trip context
    booking = models.OneToOneField(
        "bookings.Booking", on_delete=models.CASCADE, related_name="chat_thread"
    )

    # Participants in the chat thread
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_chat_threads",
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_chat_threads",
    )

    # Status flags
    is_active = models.BooleanField(
        default=True,
        help_text="Set to False once the job/booking is completed or canceled to close the chat.",
    )

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["booking"]),
            models.Index(fields=["client"]),
            models.Index(fields=["driver"]),
        ]

        permissions = [
            ("can_create_thread", "Can create a chat thread"),
            ("can_read_thread", "Can read a chat thread"),
            ("can_delete_thread", "Can delete a chat thread"),
        ]

    def __str__(self):
        return f"ChatThread ({self.id}) - Booking: {self.booking_id}"
