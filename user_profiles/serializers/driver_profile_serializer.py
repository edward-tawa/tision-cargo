from rest_framework import serializers

from user_profiles.models.driver_profile_model import DriverProfile


class DriverProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DriverProfile
        fields = [
            "id",
            "user",
            "drivers_license_number",
            "vehicle_type",
            "vehicle_reg_number",
            "make_and_model",
            "max_weight_kg",
            "vehicle_front_photo",
            "vehicle_rear_photo",
            "vehicle_side_photo",
            "completed_trips_count",
            "is_available",
            "rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "completed_trips_count",
            "rating",
            "created_at",
            "updated_at",
        ]
