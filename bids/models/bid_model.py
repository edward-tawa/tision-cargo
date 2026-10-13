from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class Bid(TimeStampModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"  # Waiting for drivers
        ASSIGNED = "assigned", "Assigned"  # Driver accepted/assigned
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    # The client who posted the haulage job and set the budget/amount
    client = models.ForeignKey(
        "user_profiles.ClientProfile",  # Or your specific client reference string
        on_delete=models.CASCADE,
        related_name="bids",
        null=True,  # <-- Add this to allow empty values
        blank=True,  # <-- Add this for form validation flexibility
    )

    # The winning driver (filled once a driver is assigned)
    assigned_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_jobs",
    )

    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN
    )

    # Fixed / Static Locations
    pickup_address = models.CharField(max_length=255)
    pickup_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    pickup_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    destination_address = models.CharField(max_length=255)
    destination_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    destination_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # Goods / Cargo details
    good_1_description = models.CharField(max_length=255)
    good_1_quantity = models.PositiveIntegerField(default=1)

    good_2_description = models.CharField(max_length=255, blank=True)
    good_2_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    good_3_description = models.CharField(max_length=255, blank=True)
    good_3_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return (
            f"Job #{self.id} by Client {self.client.email} - Amount: ${self.bid_amount}"
        )

    def clean(self):
        super().clean()
        # Prevent a client from assigning themselves as the driver
        if self.assigned_driver and self.client == self.assigned_driver:
            raise ValidationError(
                {
                    "assigned_driver": "A client cannot be assigned as the driver for their own job."
                }
            )

    def save(self, *args, **kwargs):
        # Ensure clean() runs even when saving via code/services
        self.full_clean()
        super().save(*args, **kwargs)
