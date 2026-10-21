from django.db import transaction
from loguru import logger
from rest_framework.exceptions import ValidationError

from bookings.models.booking_model import Booking


class BookingCRUDService:
    """
    CRUD service class for handling database operations related to Booking objects
    using explicit keyword-only arguments.
    """

    @staticmethod
    def get_booking(booking_id):
        """
        Retrieve a single booking by its ID.
        """
        logger.info(f"Fetching Booking #{booking_id}")
        try:
            return Booking.objects.select_related("client", "assigned_driver").get(
                id=booking_id
            )
        except Booking.DoesNotExist:
            logger.error(f"Booking #{booking_id} not found.")
            raise ValidationError({"detail": f"Booking #{booking_id} does not exist."})

    @staticmethod
    def get_bookings(client=None, assigned_driver=None, booking_status=None):
        """
        Retrieve a filtered list of bookings.
        """
        logger.info(
            "Fetching bookings list with filters: client=%s, assigned_driver=%s, booking_status=%s",
            client,
            assigned_driver,
            booking_status,
        )
        queryset = Booking.objects.select_related("client", "assigned_driver").all()

        if client:
            queryset = queryset.filter(client_id=client)
        if assigned_driver:
            queryset = queryset.filter(assigned_driver_id=assigned_driver)
        if booking_status:
            queryset = queryset.filter(booking_status=booking_status)

        return queryset.order_by("-created_at")

    @staticmethod
    @transaction.atomic
    def create_booking(
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
        assigned_driver=None,
    ):
        """
        Create a new booking record using explicit keyword-only arguments.
        """
        logger.info(f"Creating new booking for client #{client}")

        booking = Booking.objects.create(
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
            assigned_driver=assigned_driver,
        )

        logger.success(f"Booking #{booking.id} successfully created.")
        return booking

    @staticmethod
    @transaction.atomic
    def update_booking(
        booking_id,
        *,
        client=None,
        assigned_driver=None,
        booking_status=None,
        budget_amount=None,
        pickup_address=None,
        pickup_lat=None,
        pickup_lng=None,
        destination_address=None,
        destination_lat=None,
        destination_lng=None,
        good_1_description=None,
        good_1_quantity=None,
        good_2_description=None,
        good_2_quantity=None,
        good_3_description=None,
        good_3_quantity=None,
    ):
        """
        Update an existing booking's details using explicit keyword-only arguments.
        """
        logger.info(f"Updating Booking #{booking_id}")
        booking = BookingCRUDService.get_booking(booking_id)

        update_data = {
            "client": client,
            "assigned_driver": assigned_driver,
            "booking_status": booking_status,
            "budget_amount": budget_amount,
            "pickup_address": pickup_address,
            "pickup_lat": pickup_lat,
            "pickup_lng": pickup_lng,
            "destination_address": destination_address,
            "destination_lat": destination_lat,
            "destination_lng": destination_lng,
            "good_1_description": good_1_description,
            "good_1_quantity": good_1_quantity,
            "good_2_description": good_2_description,
            "good_2_quantity": good_2_quantity,
            "good_3_description": good_3_description,
            "good_3_quantity": good_3_quantity,
        }

        fields_to_update = {k: v for k, v in update_data.items() if v is not None}

        for key, value in fields_to_update.items():
            setattr(booking, key, value)

        booking.save()

        logger.success(f"Booking #{booking.id} successfully updated.")
        return booking

    @staticmethod
    @transaction.atomic
    def delete_booking(booking_id):
        """
        Delete a booking record.
        """
        logger.warning(f"Deleting Booking #{booking_id}")
        booking = BookingCRUDService.get_booking(booking_id)
        booking.delete()
        logger.success(f"Booking #{booking.id} deleted successfully.")
        return True
