from django.db import transaction
from loguru import logger
from rest_framework.exceptions import ValidationError

from bids.models.bid_model import Bid


class BidCRUDService:
    """
    CRUD service class for handling database operations related to Bid objects
    using explicit keyword-only arguments.
    """

    @staticmethod
    def get_bid(bid_id):
        """
        Retrieve a single bid by its ID.
        """
        logger.info(f"Fetching Bid #{bid_id}")
        try:
            return Bid.objects.select_related("booking", "driver").get(id=bid_id)
        except Bid.DoesNotExist:
            logger.error(f"Bid #{bid_id} not found.")
            raise ValidationError({"detail": f"Bid #{bid_id} does not exist."})

    @staticmethod
    def get_bids(booking=None, driver=None, bid_status=None):
        """
        Retrieve a filtered list of bids.
        """
        logger.info(
            "Fetching bids list with filters: booking=%s, driver=%s, bid_status=%s",
            booking,
            driver,
            bid_status,
        )
        queryset = Bid.objects.select_related("booking", "driver").all()

        if booking:
            queryset = queryset.filter(booking_id=booking)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if bid_status:
            queryset = queryset.filter(bid_status=bid_status)

        return queryset.order_by("-created_at")

    @staticmethod
    @transaction.atomic
    def create_bid(
        *,
        booking,
        driver,
        bid_amount,
        driver_notes="",
    ):
        """
        Create a new driver bid record using explicit keyword-only arguments.
        """
        logger.info(
            f"Creating new bid for Booking #{booking.id if hasattr(booking, 'id') else booking} by Driver #{driver}"
        )

        bid = Bid.objects.create(
            booking=booking,
            driver=driver,
            bid_amount=bid_amount,
            driver_notes=driver_notes,
        )

        logger.success(f"Bid #{bid.id} successfully created.")
        return bid

    @staticmethod
    @transaction.atomic
    def update_bid(
        bid_id,
        *,
        bid_amount=None,
        bid_status=None,
        driver_notes=None,
    ):
        """
        Update an existing bid's details using explicit keyword-only arguments.
        """
        logger.info(f"Updating Bid #{bid_id}")
        bid = BidCRUDService.get_bid(bid_id)

        update_data = {
            "bid_amount": bid_amount,
            "bid_status": bid_status,
            "driver_notes": driver_notes,
        }

        # Filter out None values so we only modify fields that were explicitly provided
        fields_to_update = {k: v for k, v in update_data.items() if v is not None}

        for key, value in fields_to_update.items():
            setattr(bid, key, value)

        bid.save()
        logger.success(f"Bid #{bid.id} successfully updated.")
        return bid

    @staticmethod
    @transaction.atomic
    def delete_bid(bid_id):
        """
        Delete a bid record.
        """
        logger.warning(f"Deleting Bid #{bid_id}")
        bid = BidCRUDService.get_bid(bid_id)
        bid.delete()
        logger.success(f"Bid #{bid.id} deleted successfully.")
        return True
