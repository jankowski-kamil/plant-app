import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from plant import notifications
from channels.db import database_sync_to_async
from  plant.notifications.models import Notification
from channels.layers import get_channel_layer


def send_message_via_websocket(user, message: dict):
    channel_layer = get_channel_layer()
    group_name = f"user_{user.id}"
    async_to_sync(channel_layer.group_send)(group_name, message)


def build_message(user):
    notificationsList = {"message": list(Notification.objects.filter(recipient=user).values('id','text'))}
    return notificationsList

@database_sync_to_async
def getNotifications(user):
    return build_message(user)

class NotificationsConsumer(AsyncJsonWebsocketConsumer):

    async def websocket_connect(self, message):
        user = self.scope["user"]

        if not user:
            return await self.close()

        self.room_name = f"user_{user.id}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        message = await getNotifications(user)
        message["type"] = "unread_status"

        await self.channel_layer.group_send(self.room_name, message)
        return None

    async def websocket_disconnect(self, message):
        if hasattr(self, "room_name"):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def alert(self, event):
        await self.send_json(event)

    async def activity(self, event):
        await self.send_json(event)

    async def unread_status(self, event):
        await self.send_json(event)


