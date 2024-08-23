
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

django_asgi_app = get_asgi_application()

from plant.channel_config.middlewares import JWTAuthMiddlewareStack
from plant.channel_config.routing import websocket_urlpatterns



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    },
)