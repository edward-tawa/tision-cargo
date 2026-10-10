from django.db import transaction
from loguru import logger

from bids.models import Bid  # Adjust import according to your app structure


class BidCRUDService:
    """
    Service class for handling complete CRUD operations related to Bid model with loguru tracking.
    """

    @staticmethod
    @transaction.atomic
    def create_bid(
        *,
        client,
        bid_amount,
        driver=None,
        pickup_address="",
        pickup_lat=None,
        pickup_lng=None,
        destination_address="",
        destination_lat=None,
        destination_lng=None,
        good_1_description="",
        good_1_quantity=None,
        good_2_description="",
        good_2_quantity=None,
        good_3_description="",
        good_3_quantity=None,
    ):
        """
        Creates and returns a new Bid instance.
        """
        logger.info(
            f"Creating new bid for client ID: {getattr(client, 'id', client)} with amount {bid_amount}"
        )

        bid = Bid.objects.create(
            client=client,
            driver=driver,
            bid_amount=bid_amount,
            pickup_address=pickup_address,
            pickup_lat=pickup_lat,
            pickup_lng=pickup_lng,
            destination_address=destination_address,
            destination_lat=destination_lat,
            destination_lng=destination_lng,
            good_1_description=good_1_description,
            good_1_quantity=good_1_quantity,
            good_2_description=good_2_description,
            good_2_quantity=good_2_quantity,
            good_3_description=good_3_description,
            good_3_quantity=good_3_quantity,
        )

        logger.success(f"Bid successfully created with ID: {bid.bid_id}")
        return bid

    @staticmethod
    def get_bid(*, bid_id):
        """
        Retrieves a single Bid instance by its ID.
        Raises Bid.DoesNotExist if not found.
        """
        logger.debug(f"Attempting to retrieve bid with ID: {bid_id}")
        try:
            bid = Bid.objects.get(bid_id=bid_id)
            return bid
        except Bid.DoesNotExist:
            logger.warning(f"Bid with ID {bid_id} does not exist.")
            raise

    @staticmethod
    def get_bids(*, client=None, driver=None, status=None):
        """
        Retrieves a filtered queryset of bids (e.g., by client, driver, or status).
        """
        logger.debug(
            f"Fetching bids with filters - client: {client}, driver: {driver}, status: {status}"
        )
        queryset = Bid.objects.all()
        if client:
            queryset = queryset.filter(client=client)
        if driver:
            queryset = queryset.filter(driver=driver)
        if status:
            queryset = queryset.filter(bid_status=status)

        logger.debug(f"Found {queryset.count()} bids matching criteria.")
        return queryset

    @staticmethod
    @transaction.atomic
    def update_bid(*, bid_id, **kwargs):
        """
        Updates an existing Bid instance with provided fields and returns it.
        Raises Bid.DoesNotExist if not found.
        """
        logger.info(
            f"Attempting to update bid ID {bid_id} with fields: {list(kwargs.keys())}"
        )
        try:
            bid = Bid.objects.get(bid_id=bid_id)
        except Bid.DoesNotExist:
            logger.warning(f"Bid with ID {bid_id} does not exist for update.")
            raise

        # Loop through and update fields if they are provided in kwargs
        for field, value in kwargs.items():
            if hasattr(bid, field):
                setattr(bid, field, value)

        bid.full_clean()  # Runs model validation rules
        bid.save()

        logger.success(f"Bid ID {bid_id} successfully updated.")
        return bid

    @staticmethod
    @transaction.atomic
    def delete_bid(*, bid_id):
        """
        Deletes a Bid instance by its ID.
        Raises Bid.DoesNotExist if not found.
        """
        logger.info(f"Attempting to delete bid with ID: {bid_id}")
        try:
            bid = Bid.objects.get(bid_id=bid_id)
        except Bid.DoesNotExist:
            logger.warning(f"Bid with ID {bid_id} does not exist for deletion.")
            raise

        bid.delete()
        logger.success(f"Bid ID {bid_id} successfully deleted.")
        return True
