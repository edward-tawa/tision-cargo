from communications.urls.chat_message_urls import urlpatterns as chat_message_urls
from communications.urls.chat_thread_urls import urlpatterns as chat_thread_urls

urlpatterns = chat_message_urls + chat_thread_urls
