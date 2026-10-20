# notifications/services/dispatchers/booking_notifications.py
from loguru import logger

from notifications.services.crud import NotificationCRUDService


class BookingNotificationDispatcher:
    """
    Dispatcher class for sending booking-lifecycle notifications.
    """

    @staticmethod
    def send_booking_status_change_notification(booking, old_status, new_status):
        """Notifies relevant parties when a booking status shifts."""
        if old_status == new_status:
            return

        # Case 1: Booking assigned to a driver
        if new_status == "assigned" and booking.assigned_driver:
            driver = booking.assigned_driver
            message = (
                f"You have been assigned to booking #{booking.id} "
                f"from {booking.pickup_address} to {booking.destination_address}."
            )
            logger.info(
                f"Triggering booking assigned notification for driver #{driver.id}"
            )

            NotificationCRUDService.create_notification(
                recipient=driver,
                message=message,
                actor=booking.client,
                target=booking,
            )

        # Case 2: Booking completed
        elif new_status == "completed":
            # Notify Client
            client_message = f"Your booking #{booking.id} has been marked as completed."
            logger.info(
                f"Triggering completion notification for client #{booking.client.id}"
            )
            NotificationCRUDService.create_notification(
                recipient=booking.client,
                message=client_message,
                actor=booking.assigned_driver,
                target=booking,
            )

            # Notify Driver if assigned
            if booking.assigned_driver:
                driver_message = (
                    f"Booking #{booking.id} has been successfully completed."
                )
                NotificationCRUDService.create_notification(
                    recipient=booking.assigned_driver,
                    message=driver_message,
                    actor=booking.client,
                    target=booking,
                )

        # Case 3: Booking cancelled
        elif new_status == "cancelled":
            # Notify both client and assigned driver (if present) about cancellation
            recipients = [booking.client]
            if booking.assigned_driver:
                recipients.append(booking.assigned_driver)

            for recipient in recipients:
                message = f"Booking #{booking.id} has been cancelled."
                logger.info(
                    f"Triggering cancellation notification for user #{recipient.id}"
                )
                NotificationCRUDService.create_notification(
                    recipient=recipient,
                    message=message,
                    target=booking,
                )
