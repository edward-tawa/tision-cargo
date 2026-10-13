# trips/services/trip_crud_service.py
from django.db import transaction
from loguru import logger
from rest_framework.exceptions import ValidationError

from trips.models.trip_model import Trip


class TripCRUDService:
    """
    CRUD service class for handling database operations related to Trip objects.
    """

    @staticmethod
    def get_trip(trip_id):
        """
        Retrieve a single trip by its ID.
        """
        logger.info(f"Fetching Trip #{trip_id}")
        try:
            return Trip.objects.select_related("bid", "driver", "client").get(
                id=trip_id
            )
        except Trip.DoesNotExist:
            logger.error(f"Trip #{trip_id} not found.")
            raise ValidationError({"detail": f"Trip #{trip_id} does not exist."})

    @staticmethod
    def get_trips(client=None, driver=None, status=None):
        """
        Retrieve a filtered list of trips.
        """
        logger.info(
            "Fetching trips list with filters: client=%s, driver=%s, status=%s",
            client,
            driver,
            status,
        )
        queryset = Trip.objects.select_related("bid", "driver", "client").all()

        if client:
            queryset = queryset.filter(client_id=client)
        if driver:
            queryset = queryset.filter(driver_id=driver)
        if status:
            queryset = queryset.filter(trip_status=status)

        return queryset.order_by("-created_at")

    @staticmethod
    @transaction.atomic
    def create_trip(**trip_data):
        """
        Create a new trip record in the database.
        Usually triggered automatically when a driver application is accepted.
        """
        logger.info(f"Creating new trip for bid #{trip_data.get('bid')}")

        trip = Trip.objects.create(**trip_data)
        logger.success(f"Trip #{trip.id} successfully created.")
        return trip

    @staticmethod
    @transaction.atomic
    def update_trip(trip_id, **trip_data):
        """
        Update an existing trip's details (status, coordinates, etc.).
        """
        logger.info(f"Updating Trip #{trip_id} with fields: {list(trip_data.keys())}")
        trip = TripCRUDService.get_trip(trip_id)

        for key, value in trip_data.items():
            setattr(trip, key, value)

        trip.save()
        logger.success(f"Trip #{trip.id} successfully updated.")
        return trip

    @staticmethod
    @transaction.atomic
    def delete_trip(trip_id):
        """
        Delete a trip record (use with caution; typically trips are cancelled rather than deleted).
        """
        logger.warning(f"Deleting Trip #{trip_id}")
        trip = TripCRUDService.get_trip(trip_id)
        trip.delete()
        logger.success(f"Trip #{trip_id} deleted successfully.")
        return True
