# user_profiles/views/user_profiles_views.py
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from core.api_responses.responses import error_response, success_response
from user_profiles.models.client_profile_model import ClientProfile
from user_profiles.serializers.client_profile_serializer import (
    ClientProfileSerializer,
)
from user_profiles.services.user_profiles_crud_service import UserProfilesCRUDService


class ClientProfileViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientProfileSerializer

    def get_queryset(self):
        """Explicit READ for Clients"""
        user = self.request.user
        if getattr(user, "is_staff", False) or getattr(user, "role", "") == "admin":
            return ClientProfile.objects.all()
        return ClientProfile.objects.filter(user=user)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            "Client profiles retrieved successfully.", serializer.data
        )

    def retrieve(self, request, pk=None):
        try:
            profile = UserProfilesCRUDService.get_client_profile_by_id(pk)

            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to view this client profile.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(profile)
            return success_response(
                "Client profile retrieved successfully.", serializer.data
            )
        except ClientProfile.DoesNotExist:
            return error_response(
                "Client profile not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        user_id = request.data.get("user_id", request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile = UserProfilesCRUDService.create_client_profile(
            user_id=user_id, **serializer.validated_data
        )
        return success_response(
            "Client profile created successfully.",
            self.get_serializer(profile).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        try:
            profile = UserProfilesCRUDService.get_client_profile_by_id(pk)

            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to modify this client profile.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            serializer = self.get_serializer(profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            updated_profile = UserProfilesCRUDService.update_client_profile(
                pk, **serializer.validated_data
            )
            return success_response(
                "Client profile updated successfully.",
                self.get_serializer(updated_profile).data,
            )
        except ClientProfile.DoesNotExist:
            return error_response(
                "Client profile not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        try:
            profile = UserProfilesCRUDService.get_client_profile_by_id(pk)

            if profile.user != request.user and not request.user.is_staff:
                return error_response(
                    "You do not have permission to delete this profile.",
                    status_code=status.HTTP_403_FORBIDDEN,
                )

            UserProfilesCRUDService.delete_client_profile(pk)
            return success_response("Client profile deleted successfully.")
        except ClientProfile.DoesNotExist:
            return error_response(
                "Client profile not found.", status_code=status.HTTP_404_NOT_FOUND
            )
