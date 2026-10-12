from django.contrib.auth import get_user_model
from rest_framework import serializers

from bids.models.bid_model import Bid

User = get_user_model()


class BidSerializer(serializers.ModelSerializer):
    # Automatically sets the client to the currently authenticated user making the request
    client = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # Optional nested representation or read-only view of the client details if needed,
    # but HiddenField handles creation securely. If you want client email visible on read,
    # you can add a separate read-only field or serializer method field.

    assigned_driver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = Bid
        fields = [
            "id",  # Standard Django primary key (or use bid_id if explicitly defined in your model)
            "client",
            "assigned_driver",
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "bid_status",  # Status starts as 'open' by default model choice
            "assigned_driver",  # Assigned later when a driver is accepted
            "created_at",
            "updated_at",
        ]
