import uuid

from django.conf import settings
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class ChatMessage(TimeStampModel):
    """
    Represents an individual message sent inside a ChatThread.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        "communications.ChatThread", on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_chat_messages",
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["thread", "created_at"]),
        ]

    def __str__(self):
        return f"Message {self.id} by User {self.sender_id} in Thread {self.thread_id}"
