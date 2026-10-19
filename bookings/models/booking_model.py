from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class Booking(TimeStampModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"  # Waiting for driver bids
        ASSIGNED = "assigned", "Assigned"  # A bid has been accepted, driver assigned
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    # The client who posted the haulage job / load request
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_bookings",
    )

    # The winning driver (filled once a bid is accepted)
    assigned_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="accepted_bookings",
    )

    booking_status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN
    )

    # Budget / Target price set by the client (optional, or required depending on your flow)
    budget_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
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
        return f"Booking #{self.id} by Client {self.client.email} - Status: {self.booking_status}"

    def clean(self):
        super().clean()
        if self.assigned_driver and self.client == self.assigned_driver:
            raise ValidationError(
                {
                    "assigned_driver": "A client cannot be assigned as the driver for their own booking."
                }
            )

    class Meta:
        permissions = [
            ("can_create_booking", "Can create a booking"),
            ("can_accept_booking", "Can accept a booking"),
            ("can_reject_booking", "Can reject a booking"),
            ("can_cancel_booking", "Can cancel a booking"),
            ("can_complete_booking", "Can complete a booking"),
            ("can_view_booking", "Can view bookings"),
            ("can_delete_booking", "Can delete bookings"),
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
