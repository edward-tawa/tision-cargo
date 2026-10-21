from django.db import transaction
from loguru import logger
from rest_framework.exceptions import ValidationError

from communications.models.chat_message_model import ChatMessage


class ChatMessageCRUDService:
    """
    CRUD service class for handling database operations related to ChatMessage objects
    using explicit keyword-only arguments and loguru logging.
    """

    @staticmethod
    def get_message(message_id):
        """
        Retrieve a single chat message by its ID.
        """
        logger.info(f"Fetching ChatMessage #{message_id}")
        try:
            return ChatMessage.objects.select_related("thread", "sender").get(
                id=message_id
            )
        except ChatMessage.DoesNotExist:
            logger.error(f"ChatMessage #{message_id} not found.")
            raise ValidationError(
                {"detail": f"ChatMessage #{message_id} does not exist."}
            )

    @staticmethod
    def get_messages(thread=None, sender=None, is_read=None):
        """
        Retrieve a filtered list of chat messages.
        """
        logger.info(
            "Fetching messages list with filters: thread=%s, sender=%s, is_read=%s",
            thread,
            sender,
            is_read,
        )
        queryset = ChatMessage.objects.select_related("thread", "sender").all()

        if thread:
            queryset = queryset.filter(thread_id=thread)
        if sender:
            queryset = queryset.filter(sender_id=sender)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)

        return queryset.order_by("created_at")

    @staticmethod
    @transaction.atomic
    def create_message(
        *,
        thread,
        sender,
        content,
        is_read=False,
    ):
        """
        Create a new chat message record using explicit keyword-only arguments.
        """
        logger.info(
            f"Creating new chat message in Thread #{thread.id if hasattr(thread, 'id') else thread} by Sender #{sender.id if hasattr(sender, 'id') else sender}"
        )

        message = ChatMessage.objects.create(
            thread=thread,
            sender=sender,
            content=content,
            is_read=is_read,
        )

        logger.success(f"ChatMessage #{message.id} successfully created.")
        return message

    @staticmethod
    @transaction.atomic
    def update_message(
        message_id,
        *,
        content=None,
        is_read=None,
    ):
        """
        Update an existing chat message's details using explicit keyword-only arguments.
        """
        logger.info(f"Updating ChatMessage #{message_id}")
        message = ChatMessageCRUDService.get_message(message_id)

        update_data = {
            "content": content,
            "is_read": is_read,
        }

        # Filter out None values so we only modify fields that were explicitly provided
        fields_to_update = {k: v for k, v in update_data.items() if v is not None}

        for key, value in fields_to_update.items():
            setattr(message, key, value)

        message.save()
        logger.success(f"ChatMessage #{message.id} successfully updated.")
        return message

    @staticmethod
    @transaction.atomic
    def delete_message(message_id):
        """
        Delete a chat message record.
        """
        logger.warning(f"Deleting ChatMessage #{message_id}")
        message = ChatMessageCRUDService.get_message(message_id)
        message.delete()
        logger.success(f"ChatMessage #{message.id} deleted successfully.")
        return True
