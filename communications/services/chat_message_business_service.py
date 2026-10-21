from django.db import transaction
from loguru import logger
from notifications.services.dispatchers.communications.chat_notification_dispatcher import (
    ChatNotificationDispatcher,
)
from rest_framework.exceptions import PermissionDenied, ValidationError

from communications.models.chat_thread_model import ChatThread
from communications.services.chat_message_crud_service import ChatMessageCRUDService


class ChatMessageBusinessService:
    """
    Business logic service class for handling operations related to chat messages,
    participant permissions, thread state validation, and notification dispatching.
    """

    @staticmethod
    @transaction.atomic
    def send_message(*, thread_id, sender, content):
        """
        Allows an authorized participant to send a message within an active chat thread.
        Enforces thread activity and participant permission rules.
        """
        logger.info(
            f"User #{sender.id} attempting to send a message in Thread #{thread_id}"
        )

        if not sender.is_authenticated:
            raise PermissionDenied("Authentication is required to send messages.")

        # 1. Fetch and validate the chat thread
        try:
            thread = ChatThread.objects.get(id=thread_id)
        except ChatThread.DoesNotExist:
            logger.error(f"ChatThread #{thread_id} not found.")
            raise ValidationError(
                {"detail": f"ChatThread #{thread_id} does not exist."}
            )

        # 2. Permission guard: Sender must be either the client or driver of this thread
        if sender != thread.client and sender != thread.driver:
            logger.warning(
                f"Unauthorized message attempt by User #{sender.id} in Thread #{thread_id}"
            )
            raise PermissionDenied("You are not a participant in this chat thread.")

        # 3. State validation: Thread must be active
        if not thread.is_active:
            logger.error(
                f"Cannot send message: ChatThread #{thread_id} is inactive/closed."
            )
            raise ValidationError(
                {
                    "detail": "This chat thread is closed because the booking is completed or cancelled."
                }
            )

        # 4. Create the message using the CRUD service
        message = ChatMessageCRUDService.create_message(
            thread=thread,
            sender=sender,
            content=content,
        )

        # 5. Trigger notification to the other thread participant(s)
        ChatNotificationDispatcher.send_new_message_notification(message)

        logger.success(
            f"ChatMessage #{message.id} successfully created and notification dispatched."
        )
        return message

    @staticmethod
    @transaction.atomic
    def mark_message_as_read(*, message_id, user):
        """
        Allows an authorized recipient to mark an incoming message as read.
        """
        logger.info(
            f"User #{user.id} attempting to mark Message #{message_id} as read."
        )
        message = ChatMessageCRUDService.get_message(message_id)

        # Ensure the user is part of the thread and not the sender
        if user != message.thread.client and user != message.thread.driver:
            raise PermissionDenied("You do not have access to this message.")

        updated_message = ChatMessageCRUDService.update_message(
            message_id=message.id,
            is_read=True,
        )

        logger.success(f"ChatMessage #{message.id} marked as read.")
        return updated_message
