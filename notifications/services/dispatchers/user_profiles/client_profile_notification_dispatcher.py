# notifications/services/dispatchers/client_notifications.py
from loguru import logger

from notifications.services.notification_crud_service import NotificationCRUDService


class ClientProfileNotificationDispatcher:
    """
    Dispatcher class for sending client-profile-related notifications.
    """

    @staticmethod
    def send_welcome_notification(client_profile):
        """Sends a welcome message when a new client profile is successfully created."""
        user = client_profile.user
        company_text = (
            f" for {client_profile.company_name}" if client_profile.company_name else ""
        )

        message = f"Welcome to the platform! Your client profile{company_text} has been set up successfully. You can now start booking freight services."

        logger.info(f"Triggering welcome notification for client profile #{user.id}")

        NotificationCRUDService.create_notification(
            recipient=user,
            message=message,
            actor=user,
            target=client_profile,
        )
