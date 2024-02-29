from django.db import models
from user_profiles.models import CustomUser


class Chat(models.Model):
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chat_seller")
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="chat_buyer")
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['seller', 'buyer'], name='chat participants'),]

    def __str__(self):
        return f"Chat {self.pk}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.recipient} - {self.timestamp}\n{self.sender} - {self.timestamp}"


class ChatSupport(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="chat_user")
    admin = models.ManyToManyField(CustomUser, related_name="admin")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat {self.pk}"


class MessageSupport(models.Model):
    chat = models.ForeignKey(ChatSupport, on_delete=models.CASCADE, related_name="messages_support")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages_support")
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="received_messages_support")
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.recipient} - {self.timestamp}\n{self.sender} - {self.timestamp}"