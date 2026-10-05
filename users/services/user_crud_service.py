from django.db import transaction
from loguru import logger

from users.models.user_model import CustomUser


class UserCRUDService:
    """
    Service class for handling CRUD operations related to CustomUser.
    """

    @staticmethod
    @transaction.atomic
    def create_user(
        *,
        email,
        password,
        first_name,
        last_name,
        age,
        phone_number,
        role=None,
        status=None,
    ):
        """
        Create a new user with the provided details. Defaults will be applied
        if role or status are not provided.
        """
        # Build extra_fields dynamically, dropping any None values
        # so Django's model defaults can kick in safely.
        extra_fields = {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
        }

        if role is not None:
            extra_fields["role"] = role
        if status is not None:
            extra_fields["status"] = status

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            **extra_fields,
        )
        logger.info(f"User created with user id: {user.id}")
        return user

    @staticmethod
    @transaction.atomic
    def update_user(user_id, **kwargs):
        """
        Update an existing user's details.
        """
        ALLOWED = {"first_name", "last_name", "age", "phone_number", "role", "status"}
        user = CustomUser.objects.select_for_update().get(id=user_id)
        for key, value in kwargs.items():
            if key not in ALLOWED:
                raise ValueError(f"Field '{key}' cannot be updated")
            setattr(user, key, value)
        user.save(update_fields=list(kwargs))
        logger.info(f"User updated with ID: {user_id}")
        return user

    @staticmethod
    def get_user_by_id(user_id):
        """
        Retrieve a user by their ID.
        """
        return CustomUser.objects.get(id=user_id)

    @staticmethod
    @transaction.atomic
    def delete_user(user_id):
        """
        Delete a user by their ID.
        """
        user = CustomUser.objects.select_for_update().get(id=user_id)
        user_id = user.id  # Store the user ID before deletion
        user.delete()
        logger.info(f"User deleted with ID: {user_id}")
