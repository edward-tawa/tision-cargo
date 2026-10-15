# trucks/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from trucks.views.truck_views import TruckTypeViewSet, TruckViewSet

# Define an explicit application namespace boundary
# app_name = "trucks"

# Initialize the REST Framework Default Router configuration
router = DefaultRouter()

# Register resource controllers onto standard endpoint parameters
router.register(r"fleet", TruckViewSet, basename="truck")
router.register(r"types", TruckTypeViewSet, basename="truck-type")

# Explicitly export the urlpatterns array required by Django's root URLconf
urlpatterns = [
    path("", include(router.urls)),
]
