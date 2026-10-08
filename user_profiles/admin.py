# Register your models here.
from django.contrib import admin

from user_profiles.models.user_profiles_models import ClientProfile, DriverProfile

admin.site.register(DriverProfile)
admin.site.register(ClientProfile)
