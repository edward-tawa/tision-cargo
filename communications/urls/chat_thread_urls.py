from rest_framework.routers import DefaultRouter

from communications.views.chat_thread_views import ChatThreadViewSet

router = DefaultRouter()
router.register(r"", ChatThreadViewSet, basename="chat-thread")
urlpatterns = router.urls
