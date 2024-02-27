from rest_framework import serializers
from .models import CustomUser,SellerProfile
from product.serializers import Product
from Category.models import Category,PodCategory


class UserRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email_or_phone','password','password_confirm']


    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user
        
    
    
class SellerRegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = SellerProfile
        fields = ['email_or_phone','password','password_confirm','market_name','location_latitude',
                  'location_longitude',]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = SellerProfile.objects.create_user(**validated_data)
        user.is_seller = True
        user.save()
        return user
    


class VerifyCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['code']


class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email_or_phone','password']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)
    
    class Meta:
        fields = ['old_password',
                  'new_password',
                  'confirm_new_password',]

class SendCodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email_or_phone']


class ForgetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=20,write_only=True)
    confirm_password = serializers.CharField(max_length=20,write_only=True)

    class Meta:
        fields = ['password','confirm_password']



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username',
                  'surname',
                  'email_or_phone',
                  'number',
                  'gender',
                  ]
        
class SellerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerProfile
        fields = ['number',
                  'market_name',
                  'address',
                  'location_latitude',
                  'location_longitude',
                  'email_or_phone',
                  'category',
                  'instagram_link',
                  'whatsapp_link',
                  'tiktok_link',
                  'facebook_link',
                  ]
        





class PodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PodCategory
        fields = ('name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class ProductSerializerForMarket(serializers.ModelSerializer):
    category = CategorySerializer()
    podcategory = PodCategorySerializer()

    class Meta:
        model = Product
        fields = ['name','category','podcategory']
        

        
class MarketSerializer(serializers.ModelSerializer):
    products = ProductSerializerForMarket(many=True, read_only=True)
    
    class Meta:
        model = SellerProfile
        fields = ('market_name','products', 'location_latitude',
                  'location_longitude', 'number', 'email_or_phone', 'is_verified','whatsapp_link','instagram_link','facebook_link','tiktok_link')



class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    class Meta:
        fields = ['refresh_token',]