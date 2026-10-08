# Register your models here.
from django.contrib import admin

from user_profiles.models.client_profile_model import ClientProfile
from user_profiles.models.driver_profile_model import DriverProfile

admin.site.register(DriverProfile)
admin.site.register(ClientProfile)
