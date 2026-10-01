from django.contrib.auth.models import Group, Permission
from loguru import logger
from user.permissions.role_to_permissions import ROLE_TO_PERMISSIONS


def create_permission_group_mapping():
    """Create one group per role and sync its permissions from ROLE_TO_PERMISSIONS."""
    for role, permissions in ROLE_TO_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=role)

        permission_objects = []
        for permission in permissions:
            app_label, codename = permission.split(".")
            try:
                permission_objects.append(
                    Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename,
                    )
                )
            except Permission.DoesNotExist:
                logger.error(
                    "Permission '{}' not found for group '{}'", permission, role
                )

        # set() replaces the group's permissions in one go (no clear-then-add gap)
        group.permissions.set(permission_objects)
