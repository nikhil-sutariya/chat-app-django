"""
ASGI config for app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chatapp.routing import websocket_urlpatterns
from chatapp.middleware import ChatAppMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": ChatAppMiddleware(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
    ),
})
