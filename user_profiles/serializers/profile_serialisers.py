from rest_framework import serializers

from .models import AdminProfile, ClientProfile, DriverProfile


class AdminProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = AdminProfile
        fields = ['user_id', 'department', 'is_super_admin', 'created_at']


class DriverProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = DriverProfile
        fields = ['user_id', 'license_number', 'vehicle_type', 'is_available', 'rating']


class ClientProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = ClientProfile
        fields = ['user_id', 'company_name', 'billing_address', 'phone_number']
