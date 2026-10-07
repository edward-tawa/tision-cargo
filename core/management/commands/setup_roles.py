from django.core.management.base import BaseCommand

from core.permissions.permission_group_mapping import create_permission_group_mapping


class Command(BaseCommand):
    help = "Creates groups and syncs permissions from ROLE_TO_PERMISSIONS"

    def handle(self, *args, **options):
        self.stdout.write("Syncing roles and permissions...")
        create_permission_group_mapping()
        self.stdout.write(
            self.style.SUCCESS("Successfully synced all roles and permissions!")
        )
