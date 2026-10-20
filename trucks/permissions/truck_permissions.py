from core.permissions.core_permissions import CorePermission


class TruckPermission(CorePermission):
    permissions_map = {
        "list": ["trucks.can_read_truck"],
        "retrieve": ["trucks.can_read_truck"],
        "create": ["trucks.can_create_truck"],
        "update": ["trucks.can_update_truck"],
        "partial_update": ["trucks.can_update_truck"],
        "destroy": ["trucks.can_delete_truck"],
    }
