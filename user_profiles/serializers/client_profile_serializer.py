from rest_framework import serializers

from user_profiles.models.client_profile_model import ClientProfile


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ["user", "home_address", "phone_number", "created_at", "updated_at"]
