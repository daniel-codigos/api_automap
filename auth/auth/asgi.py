import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .middleware import WebSocketTokenAuthMiddleware  # Middleware para WebSocket
from .routing import ws_url  # Tus rutas de WebSocket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')

django_asgi_app = get_asgi_application()  # Para vistas HTTP

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Usa RestrictIPMiddleware para vistas HTTP
    "websocket": WebSocketTokenAuthMiddleware(  # Usa autenticación por token para WebSocket
        URLRouter(ws_url)
    ),
})
