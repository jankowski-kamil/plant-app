from django.urls import path

from plant.channel_config import consumers

websocket_urlpatterns = [
    path("ws/notifications/", consumers.NotificationsConsumer.as_asgi()),
]
