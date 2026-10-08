from rest_framework import serializers

from user_profiles.models.client_profile_model import ClientProfile


class ClientProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ClientProfile
        fields = ["user", "company_name", "home_address", "phone_number"]
