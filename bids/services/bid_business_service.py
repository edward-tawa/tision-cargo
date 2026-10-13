from django.db import transaction
from loguru import logger
from rest_framework.exceptions import PermissionDenied, ValidationError

from bids.models.bid_model import Bid
from bids.services.bid_crud_service import BidCRUDService
from bookings.services.booking_crud_service import BookingCRUDService


class BidBusinessService:
    """
    Business logic service class for handling operations related to driver bids,
    validations, permissions, and state transitions.
    """

    @staticmethod
    @transaction.atomic
    def create_bid_for_driver(
        *,
        booking_id,
        driver,
        bid_amount,
        driver_notes="",
    ):
        """
        Allows a driver to submit a price offer (bid) against an open booking.
        Enforces domain rules (booking must be open, driver cannot bid on own booking, single bid per driver).
        """
        logger.info(
            f"Driver #{driver.id} attempting to submit a bid for Booking #{booking_id}"
        )

        if not driver.is_authenticated:
            raise PermissionDenied("Authentication is required to submit a bid.")

        # 1. Fetch and validate the target booking
        booking = BookingCRUDService.get_booking(booking_id)

        if booking.booking_status != booking.Status.OPEN:
            logger.error(
                f"Cannot bid on Booking #{booking_id}: Status is '{booking.booking_status}'"
            )
            raise ValidationError(
                {"detail": "This booking is no longer open for bidding."}
            )

        # 2. Prevent a driver from bidding on their own booking (if drivers can also act as clients)
        if booking.client == driver:
            logger.warning(
                f"Driver #{driver.id} attempted to bid on their own booking #{booking_id}"
            )
            raise ValidationError(
                {"detail": "Drivers cannot bid on bookings they created."}
            )

        # 3. Prevent duplicate active bids from the same driver on the same booking
        existing_bid = Bid.objects.filter(
            booking=booking,
            driver=driver,
            bid_status__in=[Bid.Status.PENDING, Bid.Status.ACCEPTED],
        ).exists()

        if existing_bid:
            logger.warning(
                f"Driver #{driver.id} already has an active bid for Booking #{booking_id}"
            )
            raise ValidationError(
                {"detail": "You have already submitted an active bid for this booking."}
            )

        # 4. Create the bid via CRUD service
        bid = BidCRUDService.create_bid(
            booking=booking,
            driver=driver,
            bid_amount=bid_amount,
            driver_notes=driver_notes,
        )

        logger.success(
            f"Bid #{bid.id} successfully created by Driver #{driver.id} for Booking #{booking.id}"
        )
        return bid

    @staticmethod
    @transaction.atomic
    def update_bid_by_driver(
        *,
        bid_id,
        driver,
        bid_amount=None,
        driver_notes=None,
    ):
        """
        Allows a driver to update their pending bid details (e.g., adjust price or notes).
        """
        logger.info(f"Driver #{driver.id} attempting to update Bid #{bid_id}")

        bid = BidCRUDService.get_bid(bid_id)

        # 1. Permission guard: Only the bid owner can modify it
        if bid.driver != driver:
            logger.warning(
                f"Unauthorized update attempt on Bid #{bid_id} by User #{driver.id}"
            )
            raise PermissionDenied("You do not have permission to modify this bid.")

        # 2. State validation: Can only update pending bids on open bookings
        if (
            bid.bid_status != bid.Status.PENDING
            or bid.booking.booking_status != bid.booking.Status.OPEN
        ):
            raise ValidationError(
                {
                    "detail": "This bid can no longer be modified because it is no longer pending or the booking is closed."
                }
            )

        updated_bid = BidCRUDService.update_bid(
            bid_id=bid_id,
            bid_amount=bid_amount,
            driver_notes=driver_notes,
        )

        logger.success(f"Bid #{bid.id} successfully updated by Driver #{driver.id}")
        return updated_bid

    @staticmethod
    @transaction.atomic
    def cancel_bid_by_driver(*, bid_id, driver):
        """
        Allows a driver to withdraw/cancel their pending bid.
        """
        logger.info(f"Driver #{driver.id} attempting to cancel Bid #{bid_id}")

        bid = BidCRUDService.get_bid(bid_id)

        # Permission guard
        if bid.driver != driver:
            logger.warning(
                f"Unauthorized cancellation attempt on Bid #{bid_id} by User #{driver.id}"
            )
            raise PermissionDenied("You do not have permission to cancel this bid.")

        if bid.bid_status != bid.Status.PENDING:
            raise ValidationError(
                {
                    "detail": f"Only pending bids can be cancelled. Current status: {bid.bid_status}"
                }
            )

        cancelled_bid = BidCRUDService.update_bid(
            bid_id=bid_id,
            bid_status=Bid.Status.CANCELLED,
        )

        logger.success(f"Bid #{bid.id} cancelled successfully.")
        return cancelled_bid
