from rest_framework import serializers

from user_profiles.models.user_profiles_models import ClientProfile, DriverProfile


class DriverProfileSerializer(serializers.ModelSerializer):
    # The 'user' field is read-only because the URL or the logged-in user
    # will determine which User ID is used as the primary key.
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DriverProfile
        fields = ["user", "license_number", "vehicle_type", "is_available", "rating"]


class ClientProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClientProfile
        fields = ["user", "company_name", "home_address", "phone_number"]
