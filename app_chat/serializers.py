from rest_framework import serializers
from .models import Chat, Message


class MessageGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        exclude = ('chat', 'sender', 'is_read', 'timestamp')


class MessageUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('content', )


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'


class ChatSellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        exclude = ('seller', )

    def validate(self, attrs):
        if attrs['buyer'].is_seller:
            raise serializers.ValidationError("No such seller")
        return attrs


class ChatBuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        exclude = ('buyer', )

    def validate(self, attrs):
        if not attrs['seller'].is_seller:
            raise serializers.ValidationError("No such buyer")
        return attrs
