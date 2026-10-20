# communications/services/dispatchers/thread_notifications.py
from loguru import logger

from notifications.services.crud import NotificationCRUDService


class ChatThreadNotificationDispatcher:
    """
    Dispatcher class for chat thread lifecycle notifications.
    """

    @staticmethod
    def send_thread_opened_notification(chat_thread):
        """Notifies both the client and driver that a secure chat line is now open."""
        participants = [chat_thread.client, chat_thread.driver]

        for recipient in participants:
            message = (
                f"A chat channel has been opened for Booking #{chat_thread.booking_id}."
            )
            logger.info(f"Triggering thread open notification for user #{recipient.id}")

            NotificationCRUDService.create_notification(
                recipient=recipient,
                message=message,
                target=chat_thread,
            )

    @staticmethod
    def send_thread_closed_notification(chat_thread):
        """Notifies participants that the chat thread has been closed/deactivated."""
        participants = [chat_thread.client, chat_thread.driver]

        for recipient in participants:
            message = f"The chat thread for Booking #{chat_thread.booking_id} has been closed."
            logger.info(
                f"Triggering thread closed notification for user #{recipient.id}"
            )

            NotificationCRUDService.create_notification(
                recipient=recipient,
                message=message,
                target=chat_thread,
            )
