from core.permissions.core_permissions import CorePermission


class DriverProfilePermission(CorePermission):
    permissions_map = {
        "list": ["user_profiles.can_read_driver_profile"],
        "retrieve": ["user_profiles.can_read_driver_profile"],
        "create": ["user_profiles.can_create_driver_profile"],
        "update": ["user_profiles.can_update_driver_profile"],
        "partial_update": ["user_profiles.can_update_driver_profile"],
        "destroy": ["user_profiles.can_delete_driver_profile"],
    }
