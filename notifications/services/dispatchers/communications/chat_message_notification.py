# communications/services/dispatchers/chat_notifications.py
from loguru import logger

from notifications.services.crud import NotificationCRUDService


class ChatMessageNotificationDispatcher:
    """
    Dispatcher class for sending chat and messaging notifications.
    """

    @staticmethod
    def send_new_message_notification(chat_message):
        """Notifies the other participant(s) in the chat thread about a new message."""
        thread = chat_message.thread
        sender = chat_message.sender

        # Assuming your ChatThread has a method or property to get participants
        # e.g., thread.get_other_participants(sender) or related fields
        recipients = thread.participants.exclude(id=sender.id)

        for recipient in recipients:
            preview_text = (
                chat_message.content[:50] + "..."
                if len(chat_message.content) > 50
                else chat_message.content
            )
            message = f"New message from {sender.first_name or sender.email}: '{preview_text}'"

            logger.info(
                f"Triggering new message notification for user #{recipient.id} in thread #{thread.id}"
            )

            NotificationCRUDService.create_notification(
                recipient=recipient,
                message=message,
                actor=sender,
                target=chat_message,
            )
