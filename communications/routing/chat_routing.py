from django.urls import re_path

from communications.consumers.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    # Matches ws://yourdomain.com/ws/chat/<uuid-thread-id>/
    re_path(r"ws/chat/(?P<thread_id>[0-9a-f-]+)/$", ChatConsumer.as_asgi()),
]
