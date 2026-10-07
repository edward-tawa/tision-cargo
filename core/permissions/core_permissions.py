from rest_framework.permissions import BasePermission


class CorePermission(BasePermission):
    """
    Custom permission class to check if the user has the required permissions
    based on the view's current action.
    """

    # Subclasses will override this dictionary with their action-to-permission mappings
    permissions_map = {}

    def has_permission(self, request, view):
        """
        Check if the user has the required permissions for the current action.
        """
        user = request.user
        if not user.is_authenticated:
            return False

        # 1. Get the current action from the view (e.g., 'list', 'create', 'accept_bid')
        action = getattr(view, "action", None)

        # 2. Look up the required permissions list for this specific action
        required_perms = self.permissions_map.get(action, [])

        # If no permissions are explicitly mapped for this action, allow by default
        # (or change to False if you want a default-deny policy)
        if not required_perms:
            return True

        # 3. Check if the user has every permission in the list
        for perm in required_perms:
            if not user.has_perm(perm):
                return False

        return True
