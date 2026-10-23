import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get("user")

        # 1. Reject unauthenticated users FIRST
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return

        # 2. Now it is safe to use self.user.id
        self.room_group_name = f"notifications_{self.user.id}"

        # 3. Add to room group and accept connections
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up group membership if the user was successfully added
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data):
        # Notifications are usually server-to-client, so clients rarely send data here,
        # but you can handle things like marking a notification as read client-to-server.
        try:
            data = json.loads(text_data)
            action = data.get("action")
            # handle client actions if needed...
        except json.JSONDecodeError:
            return

    async def send_notification(self, event):
        """
        Triggered when channel_layer.group_send targets this room group.
        Matches the 'type': 'send_notification' in your backend code.
        """
        notification_data = event.get("notification")
        await self.send(text_data=json.dumps(notification_data))
