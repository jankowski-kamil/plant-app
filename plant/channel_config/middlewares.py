from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware
from django.conf import settings
from django.db import close_old_connections
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        jwt_cookie = scope["cookies"].get(settings.REST_AUTH["JWT_AUTH_COOKIE"], "")
        await self.authenticate_user(scope, jwt_cookie)

        return await self.inner(scope, receive, send)

    async def authenticate_user(self, scope, jwt_cookie):
        try:
            auth = JWTAuthentication()
            validated_token = auth.get_validated_token(jwt_cookie)
            scope["user"] = await database_sync_to_async(auth.get_user)(validated_token)
        except InvalidToken:
            scope["user"] = None


def JWTAuthMiddlewareStack(inner):  # noqa: N802
    return CookieMiddleware(JWTAuthMiddleware(inner))
