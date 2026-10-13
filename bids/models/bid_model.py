from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class Bid(TimeStampModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        CANCELLED = "cancelled", "Cancelled"

    # The booking this bid is being submitted for
    booking = models.ForeignKey(
        "bookings.Booking",
        on_delete=models.CASCADE,
        related_name="bids",
    )

    # The driver submitting the price offer
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_bids",
    )

    # The price proposed by the driver
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    bid_status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    # Optional notes from the driver (e.g., "Can pick up 1 hour earlier")
    driver_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Bid #{self.id} by Driver {self.driver.email} for Booking #{self.booking.id} - Amount: ${self.bid_amount}"

    def clean(self):
        super().clean()
        # Ensure a driver can't bid on a booking posted by themselves (if drivers can also be clients)
        if hasattr(self, "booking") and self.booking.client == self.driver:
            raise ValidationError(
                {"driver": "Drivers cannot bid on their own bookings."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
