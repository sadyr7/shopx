import json
from app_chat.models import Chat, Message
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        if self.scope["user"] is not AnonymousUser:
            self.user = self.scope["user"]
            self.chat = Chat.objects.filter(pk=self.scope['url_route']['kwargs']['id'])
            await self.channel_layer.group_add(f"{self.user.id}-message", self.channel_name)

    async def send_info_to_user_group(self, event):
        message = event["text"]
        await self.send(text_data=json.dumps(message))

    async def send_last_message(self, event):
        last_msg = await self.get_last_message(self.user, self.chat)
        last_msg["status"] = event["text"]
        await self.send(text_data=json.dumps(last_msg))

    @database_sync_to_async
    def get_last_message(self, user, chat):
        message = Message.objects.filter(recipient=user, chat=chat).order_by('timestamp').first()
        return message.content

    async def disconnect(self, close_code):
        pass
