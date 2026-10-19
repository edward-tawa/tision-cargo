from core.permissions.core_permissions import CorePermission


class TripPermission(CorePermission):
    permissions_map = {
        "list": ["trips.can_view_trip"],
        "retrieve": ["trips.can_view_trip"],
        "create": ["trips.can_create_trip"],
        "update": ["trips.can_change_trip"],
        "partial_update": ["trips.can_change_trip"],
        "destroy": ["trips.can_delete_trip"],
    }
