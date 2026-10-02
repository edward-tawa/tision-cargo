from django.db import transaction
from loguru import logger

from users.models.user_model import CustomUser


class UserBusinessService:
    """Business actions that change a user's status or role."""

    # ---------- Status ----------

    @staticmethod
    @transaction.atomic
    def activate_user(user_id, *, actor_id=None):
        """Set the user's status to VERIFIED."""
        user = CustomUser.objects.select_for_update().get(id=user_id)
        old_status = user.status
        if old_status == CustomUser.STATUS.VERIFIED:
            return user

        user.status = CustomUser.STATUS.VERIFIED
        user.save(update_fields=["status"])

        transaction.on_commit(
            lambda: logger.info(
                "User activated: user={} {} -> verified by={}",
                user_id,
                old_status,
                actor_id,
            )
        )
        return user

    @staticmethod
    @transaction.atomic
    def suspend_user(user_id, *, actor_id=None):
        """Set the user's status to SUSPENDED."""
        user = CustomUser.objects.select_for_update().get(id=user_id)
        old_status = user.status
        if old_status == CustomUser.STATUS.SUSPENDED:
            return user

        user.status = CustomUser.STATUS.SUSPENDED
        user.save(update_fields=["status"])

        transaction.on_commit(
            lambda: logger.info(
                "User suspended: user={} {} -> suspended by={}",
                user_id,
                old_status,
                actor_id,
            )
        )
        return user

    # ---------- Role ----------

    @staticmethod
    @transaction.atomic
    def make_admin(user_id, *, actor_id=None):
        """Set the user's role to ADMIN."""
        user = CustomUser.objects.select_for_update().get(id=user_id)
        old_role = user.role
        if old_role == CustomUser.ROLE.ADMIN:
            return user

        user.role = CustomUser.ROLE.ADMIN
        user.save(update_fields=["role"])

        transaction.on_commit(
            lambda: logger.info(
                "User made admin: user={} {} -> admin by={}",
                user_id,
                old_role,
                actor_id,
            )
        )
        return user

    @staticmethod
    @transaction.atomic
    def make_client(user_id, *, actor_id=None):
        """Set the user's role to CLIENT."""
        user = CustomUser.objects.select_for_update().get(id=user_id)
        old_role = user.role
        if old_role == CustomUser.ROLE.CLIENT:
            return user

        user.role = CustomUser.ROLE.CLIENT
        user.save(update_fields=["role"])

        transaction.on_commit(
            lambda: logger.info(
                "User made client: user={} {} -> client by={}",
                user_id,
                old_role,
                actor_id,
            )
        )
        return user

    @staticmethod
    @transaction.atomic
    def make_driver(user_id, *, actor_id=None):
        """Set the user's role to DRIVER."""
        user = CustomUser.objects.select_for_update().get(id=user_id)
        old_role = user.role
        if old_role == CustomUser.ROLE.DRIVER:
            return user

        user.role = CustomUser.ROLE.DRIVER
        user.save(update_fields=["role"])

        transaction.on_commit(
            lambda: logger.info(
                "User made driver: user={} {} -> driver by={}",
                user_id,
                old_role,
                actor_id,
            )
        )
        return user
