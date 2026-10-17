from rest_framework import serializers

from notifications.models_notification_model import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model, handling generic actor and target fields.
    """

    actor_type = serializers.SerializerMethodField(read_only=True)
    actor_id = serializers.SerializerMethodField(read_only=True)
    actor_repr = serializers.SerializerMethodField(read_only=True)

    target_type = serializers.SerializerMethodField(read_only=True)
    target_id = serializers.SerializerMethodField(read_only=True)
    target_repr = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "actor_type",
            "actor_id",
            "actor_repr",
            "target_type",
            "target_id",
            "target_repr",
            "message",
            "is_read",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "recipient",
            "actor_type",
            "actor_id",
            "actor_repr",
            "target_type",
            "target_id",
            "target_repr",
            "created_at",
            "updated_at",
        ]

    def get_actor_type(self, obj):
        """Returns the lowercase model name of the actor (e.g., 'truck', 'user')."""
        return obj.actor_content_type.model if obj.actor_content_type else None

    def get_actor_id(self, obj):
        """Returns the primary key ID of the actor object."""
        return obj.actor_object_id

    def get_actor_repr(self, obj):
        """Returns the string representation of the actor object."""
        return str(obj.actor) if obj.actor else None

    def get_target_type(self, obj):
        """Returns the lowercase model name of the target (e.g., 'booking', 'shipment')."""
        return obj.target_content_type.model if obj.target_content_type else None

    def get_target_id(self, obj):
        """Returns the primary key ID of the target object."""
        return obj.target_object_id

    def get_target_repr(self, obj):
        """Returns the string representation of the target object."""
        return str(obj.target_object) if obj.target_object else None
