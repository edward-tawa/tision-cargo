from django.contrib.auth import get_user_model
from django.db import transaction
from loguru import logger

from user_profiles.models.driver_profile_model import DriverProfile

User = get_user_model()


class DriverProfileCRUDService:
    """
    A service class for managing driver profiles, enhanced with Loguru logging.
    """

    @staticmethod
    def get_driver_profile_by_id(profile_id):
        logger.info(f"Fetching driver profile with ID: {profile_id}")
        try:
            profile = DriverProfile.objects.get(id=profile_id)
            logger.debug(
                f"Successfully fetched driver profile for user: {profile.user.email}"
            )
            return profile
        except DriverProfile.DoesNotExist:
            logger.warning(f"Driver profile with ID {profile_id} was not found.")
            raise

    @staticmethod
    @transaction.atomic
    def create_driver_profile(
        *,
        user_id,
        drivers_license_number,
        vehicle_type,
        vehicle_reg_number,
        make_and_model,
        max_weight_kg,
        vehicle_front_photo,
        vehicle_rear_photo,
        vehicle_side_photo,
    ):
        logger.info(f"Attempting to create driver profile for user ID: {user_id}")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            logger.error(
                f"Failed to create driver profile: User with ID {user_id} does not exist."
            )
            raise

        profile = DriverProfile.objects.create(
            user=user,
            drivers_license_number=drivers_license_number,
            vehicle_type=vehicle_type,
            vehicle_reg_number=vehicle_reg_number,
            make_and_model=make_and_model,
            max_weight_kg=max_weight_kg,
            vehicle_front_photo=vehicle_front_photo,
            vehicle_rear_photo=vehicle_rear_photo,
            vehicle_side_photo=vehicle_side_photo,
        )

        logger.success(
            f"Driver profile successfully created for user: {user.email} (ID: {user_id})"
        )
        return profile

    @staticmethod
    @transaction.atomic
    def update_driver_profile(profile_id, **profile_data):
        updated_fields = list(profile_data.keys())
        logger.info(
            f"Attempting to update driver profile ID: {profile_id} with fields: {updated_fields}"
        )

        try:
            profile = DriverProfile.objects.get(id=profile_id)
        except DriverProfile.DoesNotExist:
            logger.error(
                f"Failed to update: Driver profile with ID {profile_id} not found."
            )
            raise

        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()

        logger.success(f"Driver profile ID {profile_id} successfully updated.")
        return profile

    @staticmethod
    @transaction.atomic
    def delete_driver_profile(profile_id):
        logger.warning(f"Attempting to delete driver profile ID: {profile_id}")

        try:
            profile = DriverProfile.objects.get(id=profile_id)
        except DriverProfile.DoesNotExist:
            logger.error(
                f"Failed to delete: Driver profile with ID {profile_id} not found."
            )
            raise

        profile.delete()
        logger.success(f"Driver profile ID {profile_id} successfully deleted.")
