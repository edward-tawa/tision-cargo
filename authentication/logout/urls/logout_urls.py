from django.urls import path

from authentication.logout.views.logout_views import LogoutView

urlpatterns = [
    path("", LogoutView.as_view(), name="logout"),
]
