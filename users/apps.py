# users/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # Connect the post_migrate signal to automatically populate groups
        post_migrate.connect(populate_groups, sender=self)


def populate_groups(sender, **kwargs):
    # Importing here to prevents circular imports during app initialization
    from users.permissions.permission_group_mapping import (
        create_permission_group_mapping,
    )

    # Run your mapping function
    create_permission_group_mapping()
