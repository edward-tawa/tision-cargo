# notifications/urls.py
from rest_framework.routers import DefaultRouter

from notifications.views.notification_views import NotificationViewSet

router = DefaultRouter()
router.register(r"", NotificationViewSet, basename="notification")
urlpatterns = router.urls
