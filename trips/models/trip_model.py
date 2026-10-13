# trips/models/trip_model.py
from django.conf import settings
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class Trip(TimeStampModel):
    class Status(models.TextChoices):
        EN_ROUTE_TO_PICKUP = "en_route_to_pickup", "En Route to Pickup"
        ARRIVED_AT_PICKUP = "arrived_at_pickup", "Arrived at Pickup"
        IN_TRANSIT = "in_transit", "In Transit to Destination"
        DELIVERED = "delivered", "Delivered"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    # Linked directly to the accepted bid
    bid = models.OneToOneField(
        "bids.Bid",
        on_delete=models.CASCADE,
        related_name="trip",
    )

    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_trips",
    )

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_trips",
    )

    trip_status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.EN_ROUTE_TO_PICKUP,
    )

    # Real-time tracking coordinates (updated via API pings from the driver's app)
    current_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    current_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    last_location_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Trip #{self.id} for Bid #{self.bid.id} - Status: {self.trip_status}"
