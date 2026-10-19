from core.permissions.core_permissions import CorePermission


class BidPermission(CorePermission):
    permissions_map = {
        # Standard CRUD
        "list": ["bids.can_view_bid"],
        "retrieve": ["bids.can_view_bid"],
        "create": ["bids.can_create_bid"],
        "update": ["bids.can_change_bid"],
        "partial_update": ["bids.can_change_bid"],
        "destroy": ["bids.can_delete_bid"],  # Restricted to admin/authorized roles
        # Custom Workflow Actions (Plugged the security leak!)
        "accept": ["bids.can_accept_bid"],
        "reject": ["bids.can_reject_bid"],
        "cancel": ["bids.can_cancel_bid"],
        "complete": ["bids.can_complete_bid"],
    }
