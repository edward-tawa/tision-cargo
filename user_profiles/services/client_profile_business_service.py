from django.db import transaction
from loguru import logger

from notifications.services.dispatchers.user_profiles.client_profile_notification_dispatcher import (
    ClientProfileNotificationDispatcher,
)
from user_profiles.services.client_profile_crud_service import ClientProfileCRUDService


class ClientProfileBusinessService:
    """
    Business logic service class for handling client profile workflows and notifications.
    """

    @staticmethod
    @transaction.atomic
    def create_client_profile_workflow(
        *, user_id, default_address=None, company_name=None
    ):
        """
        Creates a client profile and triggers the welcome notification dispatcher.
        """
        logger.info(
            f"Executing client profile creation workflow for user ID: {user_id}"
        )

        profile = ClientProfileCRUDService.create_client_profile(
            user_id=user_id,
            default_address=default_address,
            company_name=company_name,
        )

        # Trigger welcome notification
        ClientProfileNotificationDispatcher.send_welcome_notification(profile)

        logger.success(f"Client profile workflow completed for user ID: {user_id}")
        return profile
