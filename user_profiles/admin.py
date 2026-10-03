# Register your models here.
from django.contrib import admin

from .models.models import ClientProfile, DriverProfile

admin.site.register(DriverProfile)
admin.site.register(ClientProfile)
