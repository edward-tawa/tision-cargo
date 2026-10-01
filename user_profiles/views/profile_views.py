from models.profiles_model import AdminProfile, ClientProfile, DriverProfile
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from serializers.profile_serialisers import (
    AdminProfileSerializer,
    ClientProfileSerializer,
    DriverProfileSerializer,
)


class AdminProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD viewset for Admin Profiles.
    """
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated]


class DriverProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD viewset for Driver Profiles.
    """
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]


class ClientProfileViewSet(viewsets.ModelViewSet):
    """
    CRUD viewset for Client Profiles.
    """
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]
