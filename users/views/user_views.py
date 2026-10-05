# users/views/user_views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action

from core.api_responses.responses import (  # Ensure error_response is imported
    error_response,
    success_response,
)
from users.models.user_model import CustomUser
from users.serializers.user_serializer import (
    CreateUserSerializer,
    ReadUserSerializer,
    UpdateUserSerializer,
)
from users.services.user_business_service import UserBusinessService
from users.services.user_crud_service import UserCRUDService


class UserViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        if self.action in ("update", "partial_update"):
            return UpdateUserSerializer
        return ReadUserSerializer

    def list(self, request):
        users = self.filter_queryset(self.get_queryset())
        return success_response(
            "Users retrieved successfully.",
            ReadUserSerializer(users, many=True).data,
        )

    def retrieve(self, request, pk=None):
        try:
            user = UserCRUDService.get_user_by_id(pk)
            return success_response(
                "User retrieved successfully.", ReadUserSerializer(user).data
            )
        except CustomUser.DoesNotExist:
            return error_response(
                "User not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Note: DRF's raise_exception=True automatically returns a formatted 400 Bad Request
        # for validation errors if your REST framework settings or custom exception handler wraps it.
        user = UserCRUDService.create_user(**serializer.validated_data)
        return success_response(
            "User created successfully.",
            ReadUserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        try:
            user = UserCRUDService.get_user_by_id(pk)
            serializer = UpdateUserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_user = UserCRUDService.update_user(pk, **serializer.validated_data)
            return success_response(
                "User updated successfully.", ReadUserSerializer(updated_user).data
            )
        except CustomUser.DoesNotExist:
            return error_response(
                "User not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):
        try:
            UserCRUDService.delete_user(pk)
            return success_response("User deleted successfully.")
        except CustomUser.DoesNotExist:
            return error_response(
                "User not found.", status_code=status.HTTP_404_NOT_FOUND
            )

    # ---- business actions ----

    @action(detail=True, methods=["post"])
    def suspend(self, request, pk=None):
        try:
            user = UserBusinessService.suspend_user(pk, actor_id=request.user.id)
            return success_response(
                "User suspended successfully.", ReadUserSerializer(user).data
            )
        except CustomUser.DoesNotExist:
            return error_response(
                "User not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return error_response(str(e), status_code=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        try:
            user = UserBusinessService.activate_user(pk, actor_id=request.user.id)
            return success_response(
                "User activated successfully.", ReadUserSerializer(user).data
            )
        except CustomUser.DoesNotExist:
            return error_response(
                "User not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return error_response(str(e), status_code=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="make-admin")
    def make_admin(self, request, pk=None):
        try:
            user = UserBusinessService.make_admin(pk, actor_id=request.user.id)
            return success_response(
                "User role changed to admin.", ReadUserSerializer(user).data
            )
        except CustomUser.DoesNotExist:
            return error_response(
                "User not found.", status_code=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return error_response(str(e), status_code=status.HTTP_400_BAD_REQUEST)
