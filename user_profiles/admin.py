# Register your models here.
from django.contrib import admin

from user_profiles.models.clients_profiles_models import ClientProfile
from user_profiles.models.driver_profiles_models import DriverProfile

admin.site.register(DriverProfile)
admin.site.register(ClientProfile)
