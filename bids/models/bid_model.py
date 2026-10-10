from django.conf import settings
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class Bid(TimeStampModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bids",
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_rides",
    )
    bid_id = models.AutoField(primary_key=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    bid_status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    # Fixed / Static Locations
    pickup_address = models.CharField(max_length=255, blank=True)
    pickup_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    pickup_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    destination_address = models.CharField(max_length=255, blank=True)
    destination_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    destination_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )

    # NEW: Goods / Cargo details (up to 3 items)
    good_1_description = models.CharField(max_length=255, blank=True)
    good_1_quantity = models.PositiveIntegerField(default=1, blank=True)

    good_2_description = models.CharField(max_length=255, blank=True)
    good_2_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    good_3_description = models.CharField(max_length=255, blank=True)
    good_3_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return f"Bid {self.bid_number} - Amount: {self.bid_amount} - Status: {self.bid_status}"

    @property
    def bid_number(self):
        if self.bid_id:
            return f"BID-{self.bid_id:05d}"
        return "BID-NEW"
