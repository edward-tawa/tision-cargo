from rest_framework import serializers

from communications.models.chat_message_model import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for individual chat messages.
    """

    sender_name = serializers.CharField(source="sender.get_full_name", read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "thread",
            "sender",
            "sender_name",
            "content",
            "is_read",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "sender", "created_at", "updated_at"]
