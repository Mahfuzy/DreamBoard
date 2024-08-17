import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DreamBoard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
        ['https://dreamboard.onrender.com']
    ),
})
