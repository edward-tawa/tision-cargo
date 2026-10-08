from django.contrib.auth import get_user_model

from user_profiles.models.client_profile_model import ClientProfile
from user_profiles.models.driver_profile_model import DriverProfile

User = get_user_model()


class UserProfilesCRUDService:
    @staticmethod
    def get_driver_profile_by_id(profile_id):
        return DriverProfile.objects.get(id=profile_id)

    @staticmethod
    def create_driver_profile(user_id, **profile_data):
        user = User.objects.get(id=user_id)
        profile = DriverProfile.objects.create(user=user, **profile_data)
        return profile

    @staticmethod
    def update_driver_profile(profile_id, **profile_data):
        profile = DriverProfile.objects.get(id=profile_id)
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
        return profile

    @staticmethod
    def get_client_profile_by_id(profile_id):
        return ClientProfile.objects.get(id=profile_id)

    @staticmethod
    def create_client_profile(user_id, **profile_data):
        user = User.objects.get(id=user_id)
        profile = ClientProfile.objects.create(user=user, **profile_data)
        return profile

    @staticmethod
    def update_client_profile(profile_id, **profile_data):
        profile = ClientProfile.objects.get(id=profile_id)
        for key, value in profile_data.items():
            setattr(profile, key, value)
        profile.save()
        return profile
