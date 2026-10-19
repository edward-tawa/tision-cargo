from core.permissions.core_permissions import CorePermission


class BookingPermission(CorePermission):
    permissions_map = {
        "list": ["bookings.can_view_booking"],
        "retrieve": ["bookings.can_view_booking"],
        "create": ["bookings.can_create_booking"],
        "update": ["bookings.can_change_booking"],
        "partial_update": ["bookings.can_change_booking"],
        "destroy": ["bookings.can_delete_booking"],
        "accept": ["bookings.can_accept_booking"],
        "reject": ["bookings.can_reject_booking"],
        "cancel": ["bookings.can_cancel_booking"],
        "complete": ["bookings.can_complete_booking"],
    }
