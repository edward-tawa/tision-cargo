"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Your application routes
    path("api/users/", include("users.urls")),
    path("api/auth/register/", include("authentication.register.urls.register_urls")),
    path("api/auth/login/", include("authentication.login.urls.login_urls")),
    path("api/auth/logout/", include("authentication.logout.urls.logout_urls")),
    path("user_profiles/clients", include("user_profiles.urls.client_profile_urls")),
    path("user_profiles/drivers", include("user_profiles.urls.drivers_profile_urls")),
    path(
        "api/auth/token/refresh/",
        include("authentication.refresh_token.urls.refresh_token_urls"),
    ),
    path("api/auth/otp/", include("authentication.otp.urls.otp_urls")),
    # --- API Documentation (drf-spectacular) ---
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
