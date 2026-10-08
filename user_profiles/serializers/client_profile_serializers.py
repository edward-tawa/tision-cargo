from rest_framework import serializers

from user_profiles.models.user_profiles_models import ClientProfile, DriverProfile


class ClientProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClientProfile
        fields = ["user", "company_name", "home_address", "phone_number"]
