from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('chat', ChatViewSet, basename='chat')
router.register('message', MessageViewSet, basename='message')

urlpatterns = [
    path('message-list/<int:pk>/', MessageListApiView.as_view(), name='message-list'),
    path('', include(router.urls)),
]
