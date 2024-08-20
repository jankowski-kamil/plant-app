from django.urls import path

from plant.channel_config import consumers

websocket_urlpatterns = [
    path(r"^ws/notifications/$", consumers.NotificationsConsumer.as_asgi()),
]