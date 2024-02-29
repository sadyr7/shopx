from django.urls import re_path
from .views import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/<int:id>/", ChatConsumer.as_asgi()),
]
