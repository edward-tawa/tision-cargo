from django.conf import settings
from django.db import models

from core.models.time_stamp_model import TimeStampModel


class DriverBidApplication(TimeStampModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    # Links to the bid posted by the client
    bid = models.ForeignKey(
        "bids.Bid", on_delete=models.CASCADE, related_name="driver_applications"
    )

    # The driver expressing interest in this bid/job
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bid_applications",
    )

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    class Meta:
        unique_together = ("bid", "driver")  # A driver can only apply once per job

    def __str__(self):
        return f"Driver {self.driver.email} applied for Job #{self.bid.id}"
