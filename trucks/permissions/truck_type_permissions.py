from core.permissions.core_permissions import CorePermission


class TruckTypePermission(CorePermission):
    permissions_map = {
        "list": ["trucks.can_read_truck_type"],
        "retrieve": ["trucks.can_read_truck_type"],
        "create": ["trucks.can_create_truck_type"],
        "update": ["trucks.can_update_truck_type"],
        "partial_update": ["trucks.can_update_truck_type"],
        "destroy": ["trucks.can_delete_truck_type"],
    }
