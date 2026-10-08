from django.urls import path

from authentication.login.views.login_views import LoginView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
]
