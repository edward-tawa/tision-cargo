from core.permissions.core_permissions import CorePermission


class ChatThreadPermission(CorePermission):
    permissions_map = {
        "list": ["communications.can_read_thread"],
        "retrieve": ["communications.can_read_thread"],
        "create": ["communications.can_create_thread"],
        "update": ["communications.can_create_thread"],
        "partial_update": ["communications.can_create_thread"],
        "destroy": ["communications.can_delete_thread"],
    }
