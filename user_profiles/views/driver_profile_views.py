from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from core.api_responses.responses import error_response, success_response
from user_profiles.models.driver_profile_model import DriverProfile
from user_profiles.serializers.driver_profile_serializer import (
    DriverProfileSerializer,
)
from user_profiles.services.driver_profile_business_service import (
    DriverProfileBusinessService,
)
from user_profiles.services.driver_profile_crud_service import DriverProfileCRUDService


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
            "Driver profiles retrieved successfully.", serializer.data
        )

    def retrieve(self, request, pk=None):
        try:
            profile = DriverProfileCRUDService.get_driver_profile_by_id(pk)

            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to view this driver profile.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(profile)
            return success_response(
                "Driver profile retrieved successfully.", serializer.data
            )
        except DriverProfile.DoesNotExist:
            return error_response(
                "Driver profile not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        user_id = request.data.get("user_id", request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Updated to call the Business Service workflow
        profile = DriverProfileBusinessService.create_driver_profile_workflow(
            user_id=user_id, **serializer.validated_data
        )
        return success_response(
            "Driver profile created successfully.",
            self.get_serializer(profile).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, pk=None):
        return self._update_profile(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update_profile(request, pk, partial=True)

    def _update_profile(self, request, pk, partial):
        try:
            profile = DriverProfileCRUDService.get_driver_profile_by_id(pk)

            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to modify this driver profile.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(
                profile, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)

            updated_profile = DriverProfileCRUDService.update_driver_profile(
                pk, **serializer.validated_data
            )
            return success_response(
                "Driver profile updated successfully.",
                self.get_serializer(updated_profile).data,
            )
        except DriverProfile.DoesNotExist:
            return error_response(
                "Driver profile not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        try:
            profile = DriverProfileCRUDService.get_driver_profile_by_id(pk)

            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to delete this profile.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            DriverProfileCRUDService.delete_driver_profile(pk)
            return success_response("Driver profile deleted successfully.")
        except DriverProfile.DoesNotExist:
            return error_response(
                "Driver profile not found.", status_code=status.HTTP_404_NOT_FOUND
            )
