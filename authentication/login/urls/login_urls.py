from rest_framework.routers import DefaultRouter

from authentication.login.views.login_view import LoginView

router = DefaultRouter()

router.register(r"", LoginView, basename="login")

urlpatterns = router.urls
