from django.db import models
from user_profiles.models import CustomUser
from solo.models import SingletonModel


class SupportService(SingletonModel):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    instagram_link = models.URLField()
    whatsapp_link = models.URLField()
    facebook_link = models.URLField()
    telegram_token = models.CharField(max_length=50)
    telegram_chat_id = models.CharField(max_length=15)

    def __str__(self):
        return "Служба поддержки"


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
