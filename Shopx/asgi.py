from channels.routing import ProtocolTypeRouter,URLRouter
import os
from notification import routing

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shopx.settings")

application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http':application,
        'websocket':URLRouter(
            routing.websocket_urlpatterns
        ),
    }
)