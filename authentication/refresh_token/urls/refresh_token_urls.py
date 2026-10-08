from django.urls import path

from authentication.refresh_token.views.refresh_token_views import (
    CustomTokenRefreshView,
)

urlpatterns = [
    path("", CustomTokenRefreshView.as_view(), name="token-refresh"),
]
