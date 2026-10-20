from core.permissions.core_permissions import CorePermission


class TruckDocumentPermission(CorePermission):
    permissions_map = {
        "list": ["trucks.can_read_truck_document"],
        "retrieve": ["trucks.can_read_truck_document"],
        "create": ["trucks.can_create_truck_document"],
        "update": ["trucks.can_update_truck_document"],
        "partial_update": ["trucks.can_update_truck_document"],
        "destroy": ["trucks.can_delete_truck_document"],
    }
