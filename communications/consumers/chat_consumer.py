import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from communications.models.chat_message_model import ChatMessage
from communications.models.chat_thread_model import ChatThread


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope["url_route"]["kwargs"]["thread_id"]
        self.room_group_name = f"chat_{self.thread_id}"
        self.user = self.scope.get("user")

        # 1. Reject unauthenticated users
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        # 2. Verify user is either the client or driver for this thread
        is_participant = await self.verify_user_in_thread()
        if not is_participant:
            await self.close()
            return

        # 3. Add to room group and accept connections
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove from room group on disconnect
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Triggered when a user sends a message through the WebSocket."""
        try:
            data = json.loads(text_data)
            message_content = data.get("message", "").strip()
        except json.JSONDecodeError:
            return

        if not message_content:
            return

        # Save message to database asynchronously
        saved_message = await self.save_message(message_content)

        # Broadcast the message to everyone in the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message_event",
                "message_id": str(saved_message.id),
                "sender_id": str(self.user.id),
                "sender_name": self.user.get_full_name(),
                "content": saved_message.content,
                "created_at": saved_message.created_at.isoformat(),
            },
        )

    async def chat_message_event(self, event):
        """Sends the broadcasted event payload down to the WebSocket client."""
        await self.send(
            text_data=json.dumps(
                {
                    "id": event["message_id"],
                    "sender": event["sender_id"],
                    "sender_name": event["sender_name"],
                    "content": event["content"],
                    "created_at": event["created_at"],
                }
            )
        )

    @database_sync_to_async
    def verify_user_in_thread(self):
        try:
            thread = ChatThread.objects.get(id=self.thread_id)
            return thread.client == self.user or thread.driver == self.user
        except ChatThread.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, content):
        thread = ChatThread.objects.get(id=self.thread_id)
        return ChatMessage.objects.create(
            thread=thread, sender=self.user, content=content
        )
