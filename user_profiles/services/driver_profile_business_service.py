from django.db import transaction
from loguru import logger
from notifications.services.dispatchers.user_profiles.driver_profile_notification_dispatcher import (
    DriverProfileNotificationDispatcher,
)

from user_profiles.services.driver_profile_crud_service import DriverProfileCRUDService


class DriverProfileBusinessService:
    """
    Business logic service class for handling driver profile workflows and notifications.
    """

    @staticmethod
    @transaction.atomic
    def create_driver_profile_workflow(*, user_id, **profile_data):
        """
        Creates a driver profile and triggers the welcome/verification notification dispatcher.
        """
        logger.info(
            f"Executing driver profile creation workflow for user ID: {user_id}"
        )

        profile = DriverProfileCRUDService.create_driver_profile(
            user_id=user_id, **profile_data
        )

        # Trigger welcome / registration notification
        DriverProfileNotificationDispatcher.send_driver_welcome_notification(profile)

        logger.success(f"Driver profile workflow completed for user ID: {user_id}")
        return profile
