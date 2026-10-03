from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.models import ClientProfile, DriverProfile
from ..serializers.serializers import ClientProfileSerializer, DriverProfileSerializer


class DriverProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Explicit READ: Admins can see all driver profiles. 
        Drivers can ONLY see their own profile.
        """
        user = self.request.user
        # Assuming your colleague's user model has an 'is_staff' or 'role' field
        if getattr(user, 'is_staff', False) or getattr(user, 'role', '') == 'admin':
            return DriverProfile.objects.all()

        # Drivers can only query their own primary key
        return DriverProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        """ Explicit CREATE: Assigns the primary key """
        user_id = self.request.data.get('user_id', self.request.user.id)
        serializer.save(user_id=user_id)

    def perform_update(self, serializer):
        """ 
        Explicit UPDATE (PUT/PATCH): 
        Prevents non-admins from changing someone else's profile.
        """
        profile = self.get_object()
        if profile.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to modify this driver profile.")
        serializer.save()

    def perform_destroy(self, instance):
        """ 
        Explicit DELETE: 
        Only allows a user to delete their own profile, or an admin to do it.
        """
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this profile.")
        instance.delete()


class ClientProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ClientProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Explicit READ for Clients """
        user = self.request.user
        if getattr(user, 'is_staff', False) or getattr(user, 'role', '') == 'admin':
            return ClientProfile.objects.all()
        return ClientProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        """ Explicit CREATE for Clients """
        user_id = self.request.data.get('user_id', self.request.user.id)
        serializer.save(user_id=user_id)

    def perform_update(self, serializer):
        """ Explicit UPDATE for Clients """
        profile = self.get_object()
        if profile.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to modify this client profile.")
        serializer.save()

    def perform_destroy(self, instance):
        """ Explicit DELETE for Clients """
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to delete this profile.")
        instance.delete()
