from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from user_profiles.models import CustomUser,SellerProfile
from datetime import timezone
from Category.models import Category, PodCategory


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
    discount = models.IntegerField()
    discounted_price = models.IntegerField(null=True)
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sell_price = models.IntegerField(null=True)

    @property
    def discounted_price(self):
        return ((self.price) * (self.discount)) / 100

    @property
    def sell_price(self):
        return (self.price) - (self.discounted_price)

    class Meta:
        ordering = ["name"]

        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]


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




class ViewedProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed = models.BooleanField()
    viewed_at = models.DateTimeField(default=timezone)

    def is_recent(self):
        return self.viewed_at >= timezone - timezone.timedelta(days=1)