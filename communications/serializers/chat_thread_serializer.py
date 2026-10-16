from rest_framework import serializers

from communications.models.chat_thread_model import ChatThread
from communications.serializers.chat_message_serializer import ChatMessageSerializer


class ChatThreadListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing chat threads (e.g., chat inbox view).
    Includes the message preview safely without heavy lifting.
    """

    last_message = serializers.SerializerMethodField()
    client_name = serializers.CharField(source="client.get_full_name", read_only=True)
    driver_name = serializers.CharField(source="driver.get_full_name", read_only=True)

    class Meta:
        model = ChatThread
        fields = [
            "id",
            "booking",
            "client",
            "client_name",
            "driver",
            "driver_name",
            "is_active",
            "last_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "client", "driver", "created_at", "updated_at"]

    def get_last_message(self, obj):
        """
        Grabs the preview. If your list view uses .select_related() or
        prefetch optimization later, this stays clean.
        """
        latest_message = obj.messages.order_by("-created_at").first()
        if latest_message:
            return ChatMessageSerializer(latest_message).data
        return None


class ChatThreadDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for a single thread view.
    Strips out unnecessary overhead for a focused data payload.
    """

    client_name = serializers.CharField(source="client.get_full_name", read_only=True)
    driver_name = serializers.CharField(source="driver.get_full_name", read_only=True)

    class Meta:
        model = ChatThread
        fields = [
            "id",
            "booking",
            "client",
            "client_name",
            "driver",
            "driver_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "client", "driver", "created_at", "updated_at"]
