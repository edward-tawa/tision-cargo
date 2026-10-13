from rest_framework import serializers

from bookings.models.booking_model import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model, handling data representation
    for client load requests and haulage postings.
    """

    booking_status_display = serializers.CharField(
        source="get_booking_status_display", read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "client",
            "assigned_driver",
            "booking_status",
            "booking_status_display",
            "budget_amount",
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
            "client",
            "assigned_driver",
            "booking_status",
            "created_at",
            "updated_at",
        ]
