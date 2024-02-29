from rest_framework import serializers
from .models import Product, Recall,ViewedProduct

from drf_spectacular.utils import extend_schema_field


class ProductSerializer(serializers.ModelSerializer):
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
        'id', 'name', 'slug', 'image', 'description', 'price', 'discount', 'discounted_price', 'available', 'location',
        'created', 'updated', 'sell_price', 'rating', 'likes')

        read_only_fields = ('id', 'slug', 'user', 'created', 'updated')


class RecallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recall
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True, }, 'created': {'read_only': True, },
                        'updated': {'read_only': True, },
                        }


class ViewedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewedProduct
        fields = '__all__'