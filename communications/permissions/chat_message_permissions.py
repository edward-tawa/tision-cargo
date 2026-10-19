from core.permissions.core_permissions import CorePermission


class ChatMessagePermission(CorePermission):
    permissions_map = {
        "list": ["communications.can_read_message"],
        "retrieve": ["communications.can_read_message"],
        "create": ["communications.can_send_message"],
        "update": ["communications.can_send_message"],
        "partial_update": ["communications.can_send_message"],
        "destroy": ["communications.can_delete_message"],
    }
