from rest_framework import serializers

from bids.models.bid_model import Bid


class BidSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bid model, handling driver price proposals
    and application submissions against bookings.
    """

    bid_status_display = serializers.CharField(
        source="get_bid_status_display", read_only=True
    )

    class Meta:
        model = Bid
        fields = [
            "id",
            "booking",
            "driver",
            "bid_amount",
            "bid_status",
            "bid_status_display",
            "driver_notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "driver",
            "bid_status",
            "created_at",
            "updated_at",
        ]
