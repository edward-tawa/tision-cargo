# users/views/user_views.py
from core.responses import success_response
from rest_framework import status, viewsets
from rest_framework.decorators import action

from users.models.user_model import CustomUser
from users.serializers.user_serializers import (
    UserCreateSerializer,
    UserReadSerializer,
    UserUpdateSerializer,
)
from users.services.user_business_service import UserBusinessService
from users.services.user_crud_service import UserCRUDService


class UserViewSet(viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        if self.action in ("update", "partial_update"):
            return UserUpdateSerializer
        return UserReadSerializer

    def list(self, request):
        users = self.filter_queryset(self.get_queryset())
        return success_response(
            "Users retrieved successfully.",
            UserReadSerializer(users, many=True).data,
        )

    def retrieve(self, request, pk=None):
        user = UserCRUDService.get_user_by_id(pk)
        return success_response(
            "User retrieved successfully.", UserReadSerializer(user).data
        )

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserCRUDService.create_user(**serializer.validated_data)
        return success_response(
            "User created successfully.",
            UserReadSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, pk=None):
        user = UserCRUDService.get_user_by_id(pk)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = UserCRUDService.update_user(pk, **serializer.validated_data)
        return success_response(
            "User updated successfully.", UserReadSerializer(user).data
        )

    def destroy(self, request, pk=None):
        UserCRUDService.delete_user(pk)
        return success_response("User deleted successfully.")

    # ---- business actions ----

    @action(detail=True, methods=["post"])
    def suspend(self, request, pk=None):
        user = UserBusinessService.suspend_user(pk, actor_id=request.user.id)
        return success_response(
            "User suspended successfully.", UserReadSerializer(user).data
        )

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        user = UserBusinessService.activate_user(pk, actor_id=request.user.id)
        return success_response(
            "User activated successfully.", UserReadSerializer(user).data
        )

    @action(detail=True, methods=["post"], url_path="make-admin")
    def make_admin(self, request, pk=None):
        user = UserBusinessService.make_admin(pk, actor_id=request.user.id)
        return success_response(
            "User role changed to admin.", UserReadSerializer(user).data
        )
