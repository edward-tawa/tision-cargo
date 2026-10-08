from django.urls import path

from authentication.register.views.register_view import RegisterView

urlpatterns = [
    path("", RegisterView.as_view(), name="register"),
]
