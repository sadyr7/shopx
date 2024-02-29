from channels.routing import ProtocolTypeRouter,URLRouter
import os
<<<<<<< HEAD
from notification import routing

=======
>>>>>>> 4ad05ad356d0e93000b1fe951ec8082e1438bcb3
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from websocket.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shopx.settings")

<<<<<<< HEAD
application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http':application,
        'websocket':URLRouter(
            routing.websocket_urlpatterns
=======
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(websocket_urlpatterns)
            )
>>>>>>> 4ad05ad356d0e93000b1fe951ec8082e1438bcb3
        ),
    }
)
