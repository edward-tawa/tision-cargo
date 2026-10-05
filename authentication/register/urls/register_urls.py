from rest_framework.routers import DefaultRouter

from authentication.register.views.register_view import RegisterView

router = DefaultRouter()
router.register(r"", RegisterView, basename="register")
urlpatterns = router.urls
