from django.contrib.auth import get_user_model
from rest_framework import serializers

from bids.models.bid_model import Bid
from bids.models.driver_application_model import DriverBidApplication

User = get_user_model()


class DriverBidApplicationSerializer(serializers.ModelSerializer):
    # Explicitly declared so the client/caller must provide the driver ID in the payload
    driver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    bid = serializers.PrimaryKeyRelatedField(queryset=Bid.objects.all())

    class Meta:
        model = DriverBidApplication
        fields = [
            "id",
            "bid",
            "driver",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status",  # Status defaults to 'pending' and shouldn't be manually forced on creation
            "created_at",
            "updated_at",
        ]

    def validate_driver(self, value):
        """
        Ensure that the selected user being assigned as a driver actually has the driver role.
        """
        if getattr(value, "role", None) != "driver":
            raise serializers.ValidationError(
                "The selected user must be registered as a driver."
            )
        return value
