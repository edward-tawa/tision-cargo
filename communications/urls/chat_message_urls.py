from rest_framework.routers import DefaultRouter

from communications.views.chat_message_views import ChatMessageViewSet

router = DefaultRouter()
router.register(r"", ChatMessageViewSet, basename="chat-message")
urlpatterns = router.urls
