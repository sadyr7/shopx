from channels.routing import ProtocolTypeRouter,URLRouter
import os

from notification import routing

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from websocket.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shopx.settings")


application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http':application,
        'websocket':URLRouter(
            routing.websocket_urlpatterns)

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#                 URLRouter(websocket_urlpatterns)
#             )

#         ),
    }
)
