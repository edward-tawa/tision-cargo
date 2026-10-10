from django.db import models

from core.models.time_stamp_model import TimeStampModel


class LiveTracking(TimeStampModel):
    """
    Separated table specifically for fast, frequent GPS coordinate updates.
    Overwrites the same record for the active bid to avoid database bloat.
    """

    bid = models.OneToOneField(
        "bids.Bid", on_delete=models.CASCADE, related_name="live_location"
    )
    current_lat = models.DecimalField(max_digits=9, decimal_places=6)
    current_lng = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"Live Tracking for Bid {self.bid.bid_id}: ({self.current_lat}, {self.current_lng})"
