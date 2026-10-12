from django.contrib.auth import get_user_model
from django.db import transaction
from loguru import logger

from user_profiles.models.client_profile_model import ClientProfile

User = get_user_model()


class ClientProfileCRUDService:
    """
    A service class for managing client profiles, enhanced with Loguru logging.
    """

    @staticmethod
    def get_client_profile_by_id(profile_id):
        logger.info(f"Fetching client profile with ID: {profile_id}")
        try:
            profile = ClientProfile.objects.get(id=profile_id)
            logger.debug(
                f"Successfully fetched client profile for user: {profile.user.email}"
            )
            return profile
        except ClientProfile.DoesNotExist:
            logger.warning(f"Client profile with ID {profile_id} was not found.")
            raise

    @staticmethod
    @transaction.atomic
    def create_client_profile(*, user_id, default_address=None, company_name=None):
        logger.info(f"Attempting to create client profile for user ID: {user_id}")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error(
                f"Failed to create client profile: User with ID {user_id} does not exist."
            )
            raise

        profile = ClientProfile.objects.create(
            user=user, default_address=default_address, company_name=company_name
        )

        logger.success(
            f"Client profile successfully created for user: {user.email} (ID: {user_id})"
        )
        return profile

    @staticmethod
    @transaction.atomic
    def update_client_profile(profile_id, **profile_data):
        updated_fields = list(profile_data.keys())
        logger.info(
            f"Attempting to update client profile ID: {profile_id} with fields: {updated_fields}"
        )

        try:
            profile = ClientProfile.objects.get(id=profile_id)
        except ClientProfile.DoesNotExist:
            logger.error(
                f"Failed to update: Client profile with ID {profile_id} not found."
            )
            raise

        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()

        logger.success(f"Client profile ID {profile_id} successfully updated.")
        return profile

    @staticmethod
    @transaction.atomic
    def delete_client_profile(profile_id):
        logger.warning(f"Attempting to delete client profile ID: {profile_id}")

        try:
            profile = ClientProfile.objects.get(id=profile_id)
        except ClientProfile.DoesNotExist:
            logger.error(
                f"Failed to delete: Client profile with ID {profile_id} not found."
            )
            raise

        profile.delete()
        logger.success(f"Client profile ID {profile_id} successfully deleted.")
