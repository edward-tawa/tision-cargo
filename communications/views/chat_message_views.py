from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action

from communications.models.chat_message_model import ChatMessage
from communications.serializers.chat_message_serializer import ChatMessageSerializer
from core.api_responses.responses import success_response


class ChatMessageViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling message-level actions (like marking messages as read)
    using GenericViewSet.
    """

    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user = self.request.user
        # Restrict message access strictly to threads where the user is client or driver
        return ChatMessage.objects.filter(
            Q(thread__client=user) | Q(thread__driver=user)
        )

    @action(detail=True, methods=["patch"], url_path="read")
    def mark_as_read(self, request, pk=None):
        """
        Endpoint to mark a specific message as read:
        PATCH /api/communications/messages/<id>/read/
        """
        message = self.get_object()

        # Prevent users from marking their own messages as read if desired,
        # or just update the flag for messages received by them
        if message.sender != request.user:
            message.is_read = True
            message.save(update_fields=["is_read"])

        return success_response(
            message="Message marked as read.",
            data=self.get_serializer(message).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["patch"], url_path="mark-thread-read")
    def mark_thread_read(self, request):
        """
        Endpoint to mark all unread messages in a specific thread as read:
        PATCH /api/communications/messages/mark-thread-read/
        Payload: { "thread_id": "<uuid>" }
        """
        thread_id = request.data.get("thread_id")
        if not thread_id:
            return success_response(
                message="thread_id is required.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = self.request.user
        # Update all messages in the thread not sent by the current user
        updated_count = (
            ChatMessage.objects.filter(thread_id=thread_id, is_read=False)
            .exclude(sender=user)
            .update(is_read=True)
        )

        return success_response(
            message=f"{updated_count} messages marked as read.",
            status=status.HTTP_200_OK,
        )
