from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from loguru import logger

from bids.models.driver_bid_application_model import DriverBidApplication

User = get_user_model()


class DriverBidApplicationCRUDService:
    """
    A service class for managing driver applications on client bids/jobs,
    enhanced with Loguru logging.
    """

    @staticmethod
    def get_bid_applications(bid_id=None, driver_id=None, status_val=None):
        """Fetch filtered list of applications for the viewset's list action."""
        logger.info("Fetching filtered list of driver bid applications.")
        queryset = DriverBidApplication.objects.all()
        if bid_id:
            queryset = queryset.filter(bid_id=bid_id)
        if driver_id:
            queryset = queryset.filter(driver_id=driver_id)
        if status_val:
            queryset = queryset.filter(status=status_val)
        return queryset

    @staticmethod
    def get_bid_application_by_id(bid_application_id):
        logger.info(f"Fetching driver application with ID: {bid_application_id}")
        try:
            application = DriverBidApplication.objects.get(id=bid_application_id)
            logger.debug(
                f"Successfully fetched application for Driver {application.driver.email} on Bid #{application.bid.id}"
            )
            return application
        except DriverBidApplication.DoesNotExist:
            logger.warning(
                f"Driver application with ID {bid_application_id} was not found."
            )
            raise

    @staticmethod
    @transaction.atomic
    def create_driver_bid_application(*, bid, driver):
        """
        Accepts model instances directly from serializer.validated_data.
        """
        logger.info(
            f"Attempting to create driver application for Driver ID: {driver.id} on Bid ID: {bid.id}"
        )

        try:
            application = DriverBidApplication.objects.create(
                bid=bid,
                driver=driver,
            )
        except IntegrityError:
            logger.warning(
                f"Duplicate application attempt: Driver {driver.email} already applied for Bid #{bid.id}."
            )
            raise ValueError("Driver has already applied for this bid.")

        logger.success(
            f"Driver application successfully created for Driver {driver.email} on Bid #{bid.id}"
        )
        return application

    @staticmethod
    @transaction.atomic
    def update_driver_bid_application(application_id, **application_data):
        updated_fields = list(application_data.keys())
        logger.info(
            f"Attempting to update driver application ID: {application_id} with fields: {updated_fields}"
        )

        try:
            application = DriverBidApplication.objects.get(id=application_id)
        except DriverBidApplication.DoesNotExist:
            logger.error(
                f"Failed to update: Driver application with ID {application_id} not found."
            )
            raise

        for key, value in application_data.items():
            setattr(application, key, value)
        application.save()

        logger.success(f"Driver application ID {application_id} successfully updated.")
        return application

    @staticmethod
    @transaction.atomic
    def delete_driver_bid_application(application_id):
        logger.warning(f"Attempting to delete driver application ID: {application_id}")

        try:
            application = DriverBidApplication.objects.get(id=application_id)
        except DriverBidApplication.DoesNotExist:
            logger.error(
                f"Failed to delete: Driver application with ID {application_id} not found."
            )
            raise

        application.delete()
        logger.success(f"Driver application ID {application_id} successfully deleted.")
