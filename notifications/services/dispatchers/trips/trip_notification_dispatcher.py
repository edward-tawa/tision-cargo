# trips/services/dispatchers/trip_notifications.py
from loguru import logger

from notifications.services.notification_crud_service import NotificationCRUDService


class TripNotificationDispatcher:
    """
    Dispatcher class for handling trip progress and status change notifications.
    """

    @staticmethod
    def send_trip_status_change_notification(trip, old_status, new_status):
        """Notifies the client and driver of critical trip status milestones."""
        if old_status == new_status:
            return

        client = trip.client
        driver = trip.driver

        # Define status-specific messages for the client
        client_message = None
        driver_message = None

        if new_status == "en_route_to_pickup":
            client_message = f"Your driver is now en route to the pickup location for Trip #{trip.id}."
        elif new_status == "arrived_at_pickup":
            client_message = (
                f"Your driver has arrived at the pickup location for Trip #{trip.id}."
            )
        elif new_status == "in_transit":
            client_message = f"Your cargo is now in transit and heading to the destination for Trip #{trip.id}."
        elif new_status == "delivered":
            client_message = (
                f"Your cargo has been marked as delivered for Trip #{trip.id}."
            )
            driver_message = f"Trip #{trip.id} has been marked as delivered."
        elif new_status == "completed":
            client_message = (
                f"Trip #{trip.id} has been successfully completed. Thank you!"
            )
            driver_message = f"Trip #{trip.id} is finalized. Great job!"
        elif new_status == "cancelled":
            client_message = f"Trip #{trip.id} has been cancelled."
            driver_message = f"Trip #{trip.id} has been cancelled."

        # Dispatch to Client
        if client_message:
            logger.info(
                f"Triggering trip status ({new_status}) notification for client #{client.id}"
            )
            NotificationCRUDService.create_notification(
                recipient=client,
                message=client_message,
                actor=driver,
                target=trip,
            )

        # Dispatch to Driver (if applicable)
        if driver_message:
            logger.info(
                f"Triggering trip status ({new_status}) notification for driver #{driver.id}"
            )
            NotificationCRUDService.create_notification(
                recipient=driver,
                message=driver_message,
                actor=client,
                target=trip,
            )
