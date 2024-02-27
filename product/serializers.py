from rest_framework import serializers
from pythonProject.Shopx.product.models import Product, Recall,Discount,ViewedProduct



class ProductSerializer(serializers.ModelSerializer):
    location = serializers.CharField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'podcategory', 'user', 'name', 'slug', 'image', 'description', 'price', 'location', 'rating',
            'available', 'created', 'updated', 'likes'
        )
        read_only_fields = ('id', 'slug', 'user', 'created', 'updated')


class RecallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recall
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True, }, 'created': {'read_only': True, },
                        'updated': {'read_only': True, },
                        }




class DiscountSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    discount_amount = serializers.DecimalField(max_digits=5, decimal_places=2)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ['id', 'product', 'discount_amount', 'discounted_price']

    def get_discounted_price(self, obj):

        if obj.product:
            discounted_price = obj.product.price - (obj.product.price * (obj.discount_amount / 100))
            return discounted_price
        else:
            return None


class ViewedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewedProduct
        fields = '__all__'