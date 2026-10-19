from core.permissions.core_permissions import CorePermission


class ClientProfilePermission(CorePermission):
    permissions_map = {
        "list": ["user_profiles.can_read_client_profile"],
        "retrieve": ["user_profiles.can_read_client_profile"],
        "create": ["user_profiles.can_create_client_profile"],
        "update": ["user_profiles.can_update_client_profile"],
        "partial_update": ["user_profiles.can_update_client_profile"],
        "destroy": ["user_profiles.can_delete_client_profile"],
    }
