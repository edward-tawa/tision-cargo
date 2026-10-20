from core.permissions.core_permissions import CorePermission


class TruckInsurancePermission(CorePermission):
    permissions_map = {
        "list": ["trucks.can_read_truck_insurance"],
        "retrieve": ["trucks.can_read_truck_insurance"],
        "create": ["trucks.can_create_truck_insurance"],
        "update": ["trucks.can_update_truck_insurance"],
        "partial_update": ["trucks.can_update_truck_insurance"],
        "destroy": ["trucks.can_delete_truck_insurance"],
    }
