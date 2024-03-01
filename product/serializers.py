from rest_framework import serializers
from .models import Product, Recall


class ProductSerializer(serializers.ModelSerializer):
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    likes = serializers.IntegerField(read_only=True)
    discount = serializers.IntegerField(required=False)

    def apply_discount_to_price(self, price, discount):
        if discount > 0 and discount <= 100:
            discounted_price = price - (price * discount) // 100
            return discounted_price
        else:
            return price

    def create(self, validated_data):
        discount = validated_data.get('discount')
        price = validated_data['price']
        if discount is not None:
            discounted_price = self.apply_discount_to_price(price, discount)
            validated_data['price'] = discounted_price
        return super().create(validated_data)

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'podcategory', 'user', 'name', 'slug', 'image', 'description', 'price', 'location', 'rating',
            'available', 'created', 'updated', 'likes', 'discount'
        )
        read_only_fields = ('id', 'slug', 'created', 'updated')


class RecallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recall
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True, }, 'created': {'read_only': True, },
                        'updated': {'read_only': True, },
                        }




