# notifications/services/dispatchers/user_profiles/driver_profile_notification_dispatcher.py
from loguru import logger

from notifications.services.notification_crud_service import NotificationCRUDService


class DriverProfileNotificationDispatcher:
    """
    Dispatcher class for sending driver-profile-related notifications.
    """

    @staticmethod
    def send_profile_submitted_notification(driver_profile):
        """Notifies the driver that their profile and vehicle details have been received for review."""
        user = driver_profile.user
        message = (
            f"Your driver profile for your {driver_profile.make_and_model} "
            f"({driver_profile.vehicle_reg_number}) has been submitted and is pending verification."
        )

        logger.info(f"Triggering submission notification for driver user #{user.id}")

        NotificationCRUDService.create_notification(
            recipient=user,
            message=message,
            actor=user,
            target=driver_profile,
        )

    @staticmethod
    def send_verification_status_notification(driver_profile, status, reason=None):
        """Notifies the driver whether their vehicle/driver credentials were approved or rejected."""
        user = driver_profile.user

        if status == "APPROVED":
            message = (
                f"Great news! Your driver profile and vehicle ({driver_profile.vehicle_reg_number}) "
                "have been approved. You are now ready to accept trips."
            )
        elif status == "REJECTED":
            reason_text = f" Reason: {reason}" if reason else ""
            message = (
                f"Your driver profile verification was rejected.{reason_text} "
                "Please update your vehicle details or photos and resubmit."
            )
        else:
            return

        logger.info(
            f"Triggering verification status ({status}) notification for driver user #{user.id}"
        )

        NotificationCRUDService.create_notification(
            recipient=user,
            message=message,
            actor=user,
            target=driver_profile,
        )
