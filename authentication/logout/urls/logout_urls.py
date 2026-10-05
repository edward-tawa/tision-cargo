from rest_framwork.routers import DefaultRouter

from authentication.logout.views.logout_view import LogoutView

router = DefaultRouter()
router.register(r"", LogoutView, basename="logout")
urlpatterns = router.urls
