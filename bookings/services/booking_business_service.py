from django.db import transaction
from loguru import logger
from rest_framework.exceptions import PermissionDenied, ValidationError

from bookings.services.booking_crud_service import BookingCRUDService
from trips.services.trip_business_service import TripBusinessService


class BookingBusinessService:
    """
    Business logic service class for handling complex operations
    related to bookings, state transitions, and bid acceptance.
    """

    @staticmethod
    @transaction.atomic
    def create_booking_for_client(
        *,
        client,
        pickup_address,
        destination_address,
        good_1_description,
        budget_amount=None,
        pickup_lat=None,
        pickup_lng=None,
        destination_lat=None,
        destination_lng=None,
        good_1_quantity=1,
        good_2_description="",
        good_2_quantity=None,
        good_3_description="",
        good_3_quantity=None,
    ):
        """
        Business logic wrapper to create a new booking initiated by a client.
        Ensures the client is valid and enforces domain rules.
        """
        logger.info(f"User #{client.id} attempting to create a new booking.")

        if not client.is_authenticated:
            raise PermissionDenied("Authentication is required to create a booking.")

        # Create booking via CRUD service
        booking = BookingCRUDService.create_booking(
            client=client,
            pickup_address=pickup_address,
            destination_address=destination_address,
            good_1_description=good_1_description,
            budget_amount=budget_amount,
            pickup_lat=pickup_lat,
            pickup_lng=pickup_lng,
            destination_lat=destination_lat,
            destination_lng=destination_lng,
            good_1_quantity=good_1_quantity,
            good_2_description=good_2_description,
            good_2_quantity=good_2_quantity,
            good_3_description=good_3_description,
            good_3_quantity=good_3_quantity,
        )

        logger.success(
            f"Booking #{booking.id} created successfully by client #{client.id}."
        )
        return booking

    @staticmethod
    @transaction.atomic
    def accept_driver_bid(*, booking_id, bid_id, user):
        """
        Allows a client to accept a specific driver's bid for their booking.
        Assigns the driver, updates statuses, and automatically spawns a Trip.
        """
        logger.info(
            f"User #{user.id} attempting to accept Bid #{bid_id} for Booking #{booking_id}"
        )

        booking = BookingCRUDService.get_booking(booking_id)

        # 1. Permission guard: Only the booking owner can accept bids
        if booking.client != user:
            logger.warning(
                f"Unauthorized bid acceptance attempt by User #{user.id} on Booking #{booking_id}"
            )
            raise PermissionDenied(
                "Only the client who created this booking can accept bids."
            )

        # 2. State validation: Booking must be open
        if booking.booking_status != booking.Status.OPEN:
            logger.error(
                f"Cannot accept bid: Booking #{booking_id} is in status '{booking.booking_status}'"
            )
            raise ValidationError(
                {
                    "detail": f"This booking is no longer open for bidding (Status: {booking.booking_status})."
                }
            )

        # 3. Retrieve and validate the target bid
        from bids.services.bid_crud_service import BidCRUDService

        bid = BidCRUDService.get_bid(bid_id=bid_id)

        if bid.booking_id != booking.id:
            raise ValidationError(
                {"detail": "The specified bid does not belong to this booking."}
            )

        # 4. Update Booking: Assign driver and mark as assigned
        booking.assigned_driver = bid.driver
        booking.booking_status = booking.Status.ASSIGNED
        booking.save(update_fields=["assigned_driver", "booking_status", "updated_at"])

        # 5. Update Bid statuses: Accept winning bid, reject other competing bids for this booking
        bid.bid_status = bid.Status.ACCEPTED
        bid.save(update_fields=["bid_status", "updated_at"])

        booking.bids.exclude(id=bid.id).filter(bid_status="pending").update(
            bid_status="rejected"
        )

        # 6. Automatically generate the live tracking Trip
        trip = TripBusinessService.create_trip_from_accepted_bid(
            booking=booking,
            driver=bid.driver,
            client=booking.client,
        )

        logger.success(
            f"Successfully accepted Bid #{bid.id} for Booking #{booking.id}. Trip #{trip.id} spawned."
        )
        return booking

    @staticmethod
    @transaction.atomic
    def cancel_booking(*, booking_id, user):
        """
        Allows a client to cancel an open or assigned booking.
        """
        logger.info(f"User #{user.id} attempting to cancel Booking #{booking_id}")

        booking = BookingCRUDService.get_booking(booking_id)

        # Permission guard
        if booking.client != user:
            logger.warning(
                f"Unauthorized cancellation attempt by User #{user.id} on Booking #{booking_id}"
            )
            raise PermissionDenied(
                "Only the client who created this booking can cancel it."
            )

        if booking.booking_status in [
            booking.Status.COMPLETED,
            booking.Status.CANCELLED,
        ]:
            raise ValidationError(
                {
                    "detail": f"Booking is already {booking.booking_status} and cannot be cancelled."
                }
            )

        # Update status
        booking.booking_status = booking.Status.CANCELLED
        booking.save(update_fields=["booking_status", "updated_at"])

        # Also cancel related active trips if they exist
        if hasattr(booking, "trip") and booking.trip:
            if booking.trip.trip_status not in [
                booking.trip.Status.COMPLETED,
                booking.trip.Status.CANCELLED,
            ]:
                TripBusinessService.update_trip_status(
                    trip_id=booking.trip.id,
                    new_status=booking.trip.Status.CANCELLED,
                    user=user,
                )

        logger.success(f"Booking #{booking.id} cancelled successfully.")
        return booking
