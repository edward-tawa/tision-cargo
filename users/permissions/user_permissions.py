from core.permissions.core_permissions import CorePermission


class UserPermission(CorePermission):
    """
    Custom permission class for user-related actions.
    Maps specific actions to required permissions.
    """

    permissions_map = {
        "list": ["users.view_user"],
        "create": ["users.add_user"],
        "retrieve": ["users.view_user"],
        "update": ["users.change_user"],
        "partial_update": ["users.change_user"],
        "destroy": ["users.delete_user"],
        "verify": ["users.verify_user"],
        "activate": ["users.activate_user"],
        "suspend": ["users.can_suspend_user"],
        "change_role": ["users.can_change_user_role"],
        "me": ["users.view_user"],
    }
