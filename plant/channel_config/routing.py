from django.urls import re_path

from plant.channel_config import consumers

websocket_urlpatterns = [
    re_path(r"^ws/notifications/$", consumers.NotificationsConsumer.as_asgi()),
]