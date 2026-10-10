from django.contrib.auth import get_user_model
from rest_framework import serializers

from bids.models.bid_model import Bid

User = get_user_model()


class BidSerializer(serializers.ModelSerializer):
    bid_number = serializers.ReadOnlyField()

    # You can explicitly declare them like this if you want custom behavior
    client = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )
    driver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Bid
        fields = [
            "bid_id",
            "bid_number",
            "client",
            "driver",
            "bid_amount",
            "bid_status",
            "pickup_address",
            "pickup_lat",
            "pickup_lng",
            "destination_address",
            "destination_lat",
            "destination_lng",
            "good_1_description",
            "good_1_quantity",
            "good_2_description",
            "good_2_quantity",
            "good_3_description",
            "good_3_quantity",
        ]
        read_only_fields = ["bid_id", "bid_number"]
