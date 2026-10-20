# notifications/services/dispatchers/bid_notifications.py
from loguru import logger

from notifications.services.crud import NotificationCRUDService


class BidNotificationDispatcher:
    """
    Dispatcher class for sending bid and bidding-process notifications.
    """

    @staticmethod
    def send_new_bid_notification(bid):
        """Notifies the client when a driver places a new bid."""
        if not bid.client or not bid.client.user:
            return

        client_user = bid.client.user
        driver_user = bid.assigned_driver  # Or driver reference depending on your setup

        message = f"A new bid of ${bid.bid_amount} has been placed on your booking."
        logger.info(
            f"Triggering new bid notification for client user #{client_user.id}"
        )

        NotificationCRUDService.create_notification(
            recipient=client_user,
            message=message,
            actor=driver_user,
            target=bid,
        )

    @staticmethod
    def send_bid_status_change_notification(bid, old_status, new_status):
        """Notifies the driver when their bid status changes (accepted, rejected, etc.)."""
        if old_status == new_status or not bid.assigned_driver:
            return

        driver_user = bid.assigned_driver

        if new_status == "accepted":
            message = (
                f"Congratulations! Your bid of ${bid.bid_amount} has been accepted."
            )
        elif new_status == "rejected":
            message = f"Your bid of ${bid.bid_amount} was declined by the client."
        elif new_status == "cancelled":
            message = f"The bid of ${bid.bid_amount} has been cancelled."
        else:
            return

        logger.info(
            f"Triggering bid status ({new_status}) notification for driver #{driver_user.id}"
        )

        NotificationCRUDService.create_notification(
            recipient=driver_user,
            message=message,
            actor=driver_user,  # Or client depending on who took the action
            target=bid,
        )
