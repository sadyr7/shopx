from typing import Iterable
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from user_profiles.models import CustomUser,SellerProfile
from Category.models import Category, PodCategory
from notification.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    podcategory = models.ForeignKey(
        PodCategory, related_name="pod_products", on_delete=models.CASCADE
    )
    user = models.ForeignKey(SellerProfile,related_name='products', on_delete=models.CASCADE,limit_choices_to={'is_seller': True})
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]
    def __str__(self):
        return self.name


class Recall(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    file = models.FileField(upload_to="recalls/%Y/%m/%d", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} {self.product}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Discount(models.Model):
    product = models.OneToOneField(
        Product, related_name="discount", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def discounted_price(self):
        return self.price * (1 - self.discount_rate)

    def __str__(self):
        return f"Discount for {self.product.name}"
    

    def save(self, *args, **kwargs):
        # Создание нового уведомления
        message = f'название продукта {self.product.name} и название магазина {self.product.user.market_name} и владелец магазина {self.product.user.username}'
        notification = Notification.objects.create(message=message)

        # Получение всех уведомлений из базы данных
        notifications = Notification.objects.all()

        # Извлечение только атрибута "message" из каждого уведомления
        message_list = [notif.message for notif in notifications]

        # Отправка уведомлений всем клиентам в группе
        channel_layer = get_channel_layer()
        
        async_to_sync(channel_layer.group_send)('notifications', {
            'type': 'send_notification',
            'message': message_list
        })

        super().save(*args, **kwargs)