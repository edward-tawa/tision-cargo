# trips/serializers/trip_serializer.py
from rest_framework import serializers

from trips.models.trip_model import Trip


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for the Trip model, handling data representation
    for active trips and historical logs.
    """

    trip_status_display = serializers.CharField(
        source="get_trip_status_display", read_only=True
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "bid",
            "driver",
            "client",
            "trip_status",
            "trip_status_display",
            "current_lat",
            "current_lng",
            "last_location_update",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "bid",
            "driver",
            "client",
            "last_location_update",
            "created_at",
            "updated_at",
        ]
