from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user_profiles.views.client_profile_views import (
    ClientProfileViewSet,
)

# Create a router and register our viewsets.
router = DefaultRouter()

router.register(
    r"user_profiles/clients", ClientProfileViewSet, basename="client-profile"
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]
