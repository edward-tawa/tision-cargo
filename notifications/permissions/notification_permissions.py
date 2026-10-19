from core.permissions.core_permissions import CorePermission


class NotificationPermission(CorePermission):
    permissions_map = {
        "list": ["notifications.can_read_notification"],
        "retrieve": ["notifications.can_read_notification"],
        "create": ["notifications.can_create_notification"],
        "update": ["notifications.can_create_notification"],
        "partial_update": ["notifications.can_create_notification"],
        "destroy": ["notifications.can_delete_notification"],
    }
