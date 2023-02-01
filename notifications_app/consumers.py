# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['user'])
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "notification_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from room group
    async def send_notification(self, event):
        print("inside send_notification function in consumers")
        print(event)
        message = event["message"]
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
