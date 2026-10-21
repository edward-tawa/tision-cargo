# trips/services/trip_business_service.py
from django.db import transaction
from django.utils import timezone
from loguru import logger
from notifications.services.dispatchers.trips.trip_notification_dispatcher import (
    TripNotificationDispatcher,
)
from rest_framework.exceptions import ValidationError

from trips.models.trip_model import Trip
from trips.services.trip_crud_service import TripCRUDService


class TripBusinessService:
    """
    Service class for handling complex business logic related to trips,
    status milestones, and live location updates.
    """

    @staticmethod
    @transaction.atomic
    def create_trip_from_accepted_bid(bid, driver, client):
        """
        Automatically creates a trip when a driver application is accepted.
        Enforces that the driver does not have another active/in-progress trip.
        """
        logger.info(
            f"Attempting to create trip for Bid #{bid.id}, Driver {driver.email}"
        )

        # 1. Enforce rule: Driver can only have one active trip at a time
        active_statuses = [
            Trip.Status.EN_ROUTE_TO_PICKUP,
            Trip.Status.ARRIVED_AT_PICKUP,
            Trip.Status.IN_TRANSIT,
            Trip.Status.DELIVERED,
        ]
        has_active_trip = Trip.objects.filter(
            driver=driver, trip_status__in=active_statuses
        ).exists()

        if has_active_trip:
            logger.error(f"Driver {driver.email} already has an active trip.")
            raise ValidationError(
                {
                    "detail": "This driver currently has an active trip and cannot be assigned to a new one."
                }
            )

        # 2. Prevent duplicate trips for the same bid
        if hasattr(bid, "trip") and bid.trip:
            logger.error(f"Trip already exists for Bid #{bid.id}")
            raise ValidationError(
                {"detail": "A trip has already been created for this bid."}
            )

        # 3. Create the Trip
        trip = Trip.objects.create(
            bid=bid,
            driver=driver,
            client=client,
            trip_status=Trip.Status.EN_ROUTE_TO_PICKUP,
        )

        # 4. Trigger initial trip notification (passing None or initial state)
        TripNotificationDispatcher.send_trip_status_change_notification(
            trip, old_status=None, new_status=trip.trip_status
        )

        logger.success(
            f"Trip #{trip.id} successfully created and linked to Bid #{bid.id}."
        )
        return trip

    @staticmethod
    @transaction.atomic
    def update_trip_status(trip_id, new_status, user):
        """
        Progresses the trip through its operational milestones.
        Validates allowed state transitions and ensures the user has permissions.
        """
        logger.info(
            f"User {user.email} attempting to update Trip #{trip_id} status to {new_status}"
        )
        trip = TripCRUDService.get_trip(trip_id)

        # Ensure user is either the assigned driver or the client
        if user != trip.driver and user != trip.client:
            logger.warning(
                f"Unauthorized status update attempt by user {user.email} on Trip #{trip_id}"
            )
            raise ValidationError(
                {"detail": "You do not have permission to update this trip's status."}
            )

        # Define allowed linear workflow transitions
        valid_transitions = {
            Trip.Status.EN_ROUTE_TO_PICKUP: [
                Trip.Status.ARRIVED_AT_PICKUP,
                Trip.Status.CANCELLED,
            ],
            Trip.Status.ARRIVED_AT_PICKUP: [
                Trip.Status.IN_TRANSIT,
                Trip.Status.CANCELLED,
            ],
            Trip.Status.IN_TRANSIT: [Trip.Status.DELIVERED, Trip.Status.CANCELLED],
            Trip.Status.DELIVERED: [Trip.Status.COMPLETED],
            Trip.Status.COMPLETED: [],
            Trip.Status.CANCELLED: [],
        }

        current_status = trip.trip_status
        allowed_next_states = valid_transitions.get(current_status, [])

        if new_status not in allowed_next_states:
            logger.error(
                f"Invalid status transition from {current_status} to {new_status} for Trip #{trip_id}"
            )
            raise ValidationError(
                {
                    "trip_status": f"Cannot transition trip state from '{current_status}' to '{new_status}'."
                }
            )

        trip.trip_status = new_status
        trip.save(update_fields=["trip_status", "updated_at"])

        # Notify relevant parties about the status change
        TripNotificationDispatcher.send_trip_status_change_notification(
            trip, old_status=current_status, new_status=new_status
        )

        logger.success(f"Trip #{trip.id} status successfully updated to {new_status}.")
        return trip

    @staticmethod
    @transaction.atomic
    def update_driver_location(trip_id, lat, lng, user):
        """
        Updates the real-time GPS coordinates of the trip.
        Strictly restricted to the assigned driver during active tracking phases.
        """
        logger.info(
            f"Driver {user.email} pushing coordinates for Trip #{trip_id}: ({lat}, {lng})"
        )
        trip = TripCRUDService.get_trip(trip_id)

        # Only the assigned driver can send location updates
        if user != trip.driver:
            logger.warning(
                f"Unauthorized location push by user {user.email} on Trip #{trip_id}"
            )
            raise ValidationError(
                {"detail": "Only the assigned driver can update trip coordinates."}
            )

        # Ensure tracking only happens while the trip is live
        active_tracking_statuses = [
            Trip.Status.EN_ROUTE_TO_PICKUP,
            Trip.Status.ARRIVED_AT_PICKUP,
            Trip.Status.IN_TRANSIT,
        ]
        if trip.trip_status not in active_tracking_statuses:
            logger.warning(
                f"Location update rejected: Trip #{trip_id} is in status {trip.trip_status}"
            )
            raise ValidationError(
                {
                    "detail": f"Cannot track coordinates for a trip in status '{trip.trip_status}'."
                }
            )

        trip.current_lat = lat
        trip.current_lng = lng
        trip.last_location_update = timezone.now()
        trip.save(
            update_fields=[
                "current_lat",
                "current_lng",
                "last_location_update",
                "updated_at",
            ]
        )

        logger.success(f"Trip #{trip.id} location successfully updated.")
        return trip
