# user_profiles/views/user_profiles_views.py
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from core.api_responses.responses import error_response, success_response
from user_profiles.models.user_profiles_models import DriverProfile
from user_profiles.serializers.driver_profiles_serializers import (
    DriverProfileSerializer,
)
from user_profiles.services.user_profiles_crud_service import UserProfilesCRUDService


class DriverProfileViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DriverProfileSerializer

    def get_queryset(self):
        """
        Explicit READ: Admins can see all driver profiles.
        Drivers can ONLY see their own profile.
        """
        user = self.request.user
        if getattr(user, "is_staff", False) or getattr(user, "role", "") == "admin":
            return DriverProfile.objects.all()
        return DriverProfile.objects.filter(user=user)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            "Driver profiles retrieved successfully.",
            serializer.data
        )

    def retrieve(self, request, pk=None):
        try:
            profile = UserProfilesCRUDService.get_driver_profile_by_id(pk)

            # Authorization verification check
            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to view this driver profile.",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            serializer = self.get_serializer(profile)
            return success_response(
                "Driver profile retrieved successfully.",
                serializer.data
            )
        except DriverProfile.DoesNotExist:
            return error_response(
                "Driver profile not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        user_id = request.data.get("user_id", request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = UserProfilesCRUDService.create_driver_profile(
            user_id=user_id, 
            **serializer.validated_data
        )
        return success_response(
            "Driver profile created successfully.",
            self.get_serializer(profile).data,
            status=status.HTTP_201_CREATED
        )

    def partial_update(self, request, pk=None):
        try:
            profile = UserProfilesCRUDService.get_driver_profile_by_id(pk)

            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to modify this driver profile.",
                    status_code=status.HTTP_403_FORBIDDEN
                )
                
            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            updated_profile = UserProfilesCRUDService.update_driver_profile(
                pk, 
                **serializer.validated_data
            )
            return success_response(
                "Driver profile updated successfully.",
                self.get_serializer(updated_profile).data
            )
        except DriverProfile.DoesNotExist:
            return error_response(
                "Driver profile not found.",
                status_code=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        try:
            profile = UserProfilesCRUDService.get_driver_profile_by_id(pk)
            
            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to delete this profile.",
                    status_code=status.HTTP_403_FORBIDDEN
                )
                
            UserProfilesCRUDService.delete_driver_profile(pk)
            return success_response("Driver profile deleted successfully.")
        except DriverProfile.DoesNotExist:
            return error_response(
                "Driver profile not found.",
                status_code=status.HTTP_444_NOT_FOUND if hasattr(status, 'HTTP_444_NOT_FOUND') else status.HTTP_404_NOT_FOUND
            )


