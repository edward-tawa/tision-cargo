from django.urls import path

from notifications.consumers.notification_consumer import consumers

websocket_urlpatterns = [
    path("ws/notifications/", consumers.NotificationConsumer.as_asgi()),
]
