from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user_profiles.views.driver_profile_views import (
    DriverProfileViewSet,
)

# Create a router and register our viewsets.
router = DefaultRouter()
router.register(
    r"user_profiles/drivers", DriverProfileViewSet, basename="driver-profile"
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
