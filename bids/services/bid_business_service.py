from django.db import transaction
from loguru import logger
from rest_framework.exceptions import ValidationError

from bids.models.bid_model import Bid
from bids.models.driver_bid_application_model import DriverBidApplication


class BidBusinessService:
    """
    Service class for handling complex business logic related to bids,
    job assignments, and status transitions.
    """

    @staticmethod
    @transaction.atomic
    def accept_driver_bid__application(bid_id, application_id, user):
        """
        Allows a client to accept a specific driver's application for their job.
        This triggers a cascade:
        1. Validates that the requesting user owns the bid.
        2. Sets the target application to ACCEPTED.
        3. Assigns the driver to the Bid, sets bid status to ASSIGNED.
        4. Automatically REJECTS all other pending applications for this bid.
        """
        logger.info(
            f"User {user.email} attempting to accept application ID: {application_id} for Bid #{bid_id}"
        )

        # 1. Fetch and validate the Bid
        try:
            bid = Bid.objects.select_for_update().get(id=bid_id)
        except Bid.DoesNotExist:
            logger.error(f"Failed to accept application: Bid #{bid_id} not found.")
            raise ValidationError({"detail": f"Bid #{bid_id} does not exist."})

        # Ensure the user making the request is the owner of the bid
        if bid.client != user:
            logger.warning(
                f"Unauthorized acceptance attempt by user {user.email} on Bid #{bid_id}"
            )
            raise ValidationError(
                {
                    "detail": "You do not have permission to manage applications for this bid."
                }
            )

        # Ensure the bid is still open
        if bid.bid_status != Bid.Status.OPEN:
            logger.warning(
                f"Failed to accept application: Bid #{bid_id} is no longer open (status: {bid.bid_status})."
            )
            raise ValidationError(
                {
                    "detail": f"This bid is no longer open for assignment. Current status: {bid.bid_status}"
                }
            )

        # 2. Fetch and validate the Target Application
        try:
            target_application = DriverBidApplication.objects.select_for_update().get(
                id=application_id, bid=bid
            )
        except DriverBidApplication.DoesNotExist:
            logger.error(
                f"Failed to accept application: Application ID {application_id} not found for Bid #{bid_id}."
            )
            raise ValidationError(
                {
                    "detail": "The specified driver application does not exist for this bid."
                }
            )

        # Safety Check: Prevent self-assignment (Client as Driver)
        if bid.client == target_application.driver:
            logger.error(
                f"Self-assignment blocked: Client {user.email} tried to accept their own driver profile."
            )
            raise ValidationError(
                {
                    "assigned_driver": "A client cannot be assigned as the driver for their own job."
                }
            )

        # 3. Update the Target Application to Accepted
        target_application.status = DriverBidApplication.Status.ACCEPTED
        target_application.save(update_fields=["status", "updated_at"])
        logger.info(
            f"Application ID {application_id} marked as ACCEPTED for Driver {target_application.driver.email}."
        )

        # 4. Update the Bid with the Winning Driver
        bid.assigned_driver = target_application.driver
        bid.bid_status = Bid.Status.ASSIGNED
        bid.save(update_fields=["assigned_driver", "bid_status", "updated_at"])
        logger.success(
            f"Bid #{bid.id} successfully assigned to Driver {target_application.driver.email}."
        )

        # 5. Automatically reject all other pending applications for this same bid
        other_applications = DriverBidApplication.objects.filter(bid=bid).exclude(
            id=application_id
        )
        updated_count = other_applications.update(
            status=DriverBidApplication.Status.REJECTED
        )

        logger.info(
            f"Automatically rejected {updated_count} competing driver applications for Bid #{bid.id}."
        )

        return bid

    @staticmethod
    @transaction.atomic
    def cancel_bid(bid_id, user):
        """
        Allows a client to cancel an open or assigned bid.
        """
        logger.info(f"User {user.email} attempting to cancel Bid #{bid_id}")

        try:
            bid = Bid.objects.select_for_update().get(id=bid_id)
        except Bid.DoesNotExist:
            logger.error(f"Failed to cancel: Bid #{bid_id} not found.")
            raise ValidationError({"detail": f"Bid #{bid_id} does not exist."})

        if bid.client != user:
            logger.warning(
                f"Unauthorized cancellation attempt by user {user.email} on Bid #{bid_id}"
            )
            raise ValidationError(
                {"detail": "You do not have permission to cancel this bid."}
            )

        if bid.bid_status in [Bid.Status.COMPLETED, Bid.Status.CANCELLED]:
            logger.warning(
                f"Failed to cancel: Bid #{bid_id} is already in terminal state ({bid.bid_status})."
            )
            raise ValidationError(
                {"detail": f"Cannot cancel a bid that is already {bid.bid_status}."}
            )

        bid.bid_status = Bid.Status.CANCELLED
        bid.save(update_fields=["bid_status", "updated_at"])

        # Cancel all pending/accepted applications associated with this cancelled bid
        DriverBidApplication.objects.filter(bid=bid).update(
            status=DriverBidApplication.Status.REJECTED
        )

        logger.success(f"Bid #{bid.id} successfully cancelled.")
        return bid
