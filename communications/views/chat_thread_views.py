from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action

from communications.models.chat_thread_model import ChatThread
from communications.serializers.chat import (
    ChatThreadDetailSerializer,
    ChatThreadListSerializer,
)
from communications.serializers.chat_message_serializer import ChatMessageSerializer
from core.api_responses.responses import success_response


class ChatThreadViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing chat threads and fetching historical messages using GenericViewSet.
    """

    queryset = ChatThread.objects.all()

    def get_queryset(self):
        user = self.request.user
        # Restrict threads strictly to the client or driver involved
        return ChatThread.objects.filter(
            Q(client=user) | Q(driver=user)
        ).select_related("client", "driver", "booking")

    def get_serializer_class(self):
        if self.action == "list":
            return ChatThreadListSerializer
        return ChatThreadDetailSerializer

    def list(self, request):
        """
        Retrieve a list of all chat threads for the authenticated user.
        """
        threads = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(threads, many=True)

        return success_response(
            message="Chat threads retrieved successfully.",
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    def retrieve(self, request, pk=None):
        """
        Retrieve details for a specific chat thread.
        """
        thread = self.get_object()
        serializer = self.get_serializer(thread)

        return success_response(
            message="Chat thread retrieved successfully.",
            data=serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["get"], url_path="messages")
    def list_messages(self, request, pk=None):
        """
        Endpoint for the mobile app to fetch past message history for a thread:
        GET /api/communications/threads/<id>/messages/
        """
        thread = self.get_object()
        messages = thread.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)

        return success_response(
            message="Chat messages retrieved successfully.",
            data=serializer.data,
            status=status.HTTP_200_OK,
        )
