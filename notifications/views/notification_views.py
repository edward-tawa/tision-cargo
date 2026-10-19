from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from core.api_responses.responses import success_response
from notifications.models import Notification
from notifications.serializers.notification_serializer import NotificationSerializer
from notifications.services.notification_business_service import (
    NotificationBusinessService,
)
from notifications.services.notification_crud_service import NotificationCRUDService


class NotificationViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling notification retrieval, status updates, and bulk actions
    restricted to the authenticated user.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """
        Ensure users can only ever access their own notifications.
        """
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Notification.objects.all()
        return Notification.objects.filter(recipient=user)

    def list(self, request):
        """
        Retrieve a list of notifications for the authenticated user,
        optionally filtered by `is_read` status.
        """
        is_read_param = request.query_params.get("is_read")
        is_read = None
        if is_read_param is not None:
            is_read = is_read_param.lower() in ["true", "1", "yes"]

        notifications = NotificationCRUDService.get_notifications(
            recipient=request.user,
            is_read=is_read,
        )
        notifications = self.filter_queryset(notifications)

        return success_response(
            message="Notifications retrieved successfully.",
            data=NotificationSerializer(notifications, many=True).data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        """
        Retrieve a single notification by its ID.
        """
        notification = NotificationCRUDService.get_notification(notification_id=pk)

        # Ownership check / Permission check
        if notification.recipient != request.user and not request.user.is_staff:
            raise PermissionDenied(
                "You do not have permission to view this notification."
            )

        return success_response(
            message="Notification retrieved successfully.",
            data=NotificationSerializer(notification).data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, pk=None):
        return self._update_notification(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update_notification(request, pk, partial=True)

    def _update_notification(self, request, pk, partial):
        """
        Update an existing notification (e.g., mark as read).
        """
        serializer = NotificationSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        updated_notification = NotificationBusinessService.mark_notification_as_read(
            notification_id=pk,
            user=request.user,
        )

        return success_response(
            message="Notification updated successfully.",
            data=NotificationSerializer(updated_notification).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        """
        Delete a notification record.
        """
        NotificationBusinessService.delete_user_notification(
            notification_id=pk,
            user=request.user,
        )
        return success_response(
            message="Notification deleted successfully.",
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="mark-all-read")
    def mark_all_read(self, request):
        """
        Endpoint to mark all unread notifications for the authenticated user as read.
        """
        updated_count = NotificationBusinessService.mark_all_user_notifications_as_read(
            user=request.user,
        )

        return success_response(
            message=f"Successfully marked {updated_count} notifications as read.",
            data={"updated_count": updated_count},
            status=status.HTTP_200_OK,
        )
