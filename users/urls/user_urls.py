# users/urls/user_urls.py
from rest_framework.routers import DefaultRouter

from users.views.user_views import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet, basename="user")

urlpatterns = router.urls
