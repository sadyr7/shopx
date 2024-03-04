from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models import ChatSupport, MessageSupport
from .serializers import *
from user_profiles.models import CustomUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q, Count


class ChatViewSet(GenericViewSet):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, ) 
    queryset = Chat.objects.all()

    def list(self, request, *args, **kwargs):
        if self.request.user.is_seller:
            queryset = (Chat.objects.filter(seller=self.request.user).order_by('timestamp')
                        .annotate(unread=Count('message', filter=Q(message__is_read=False))))
            serializer = ChatSellerSerializer(queryset, many=True)
        else:
            queryset = (Chat.objects.filter(buyer=self.request.user).order_by('timestamp')
                        .annotate(unread=Count('message', filter=Q(message__is_read=False))))
            serializer = ChatBuyerSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if self.request.user.is_seller:
            serializer = ChatSellerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(seller=self.request.user)
        else:
            serializer = ChatBuyerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(buyer=self.request.user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.seller == self.request.user or instance.buyer == self.request.user:
            instance.delete()
            return Response('Chat is deleted')
        else:
            return Response('No access')


class MessageListApiView(ListAPIView):
    serializer_class = MessageGetSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_seller:
            chats = Chat.objects.filter(seller=self.request.user).values_list('pk', flat=True)
        else:
            chats = Chat.objects.filter(buyer=self.request.user).values_list('pk', flat=True)
        if self.kwargs['pk'] in chats:
            queryset = Message.objects.filter(chat=self.kwargs['pk']).order_by('timestamp')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response('No access')


class MessageViewSet(GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageGetSerializer
    permission_classes = (IsAuthenticated, )

    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_seller and not serializer.validated_data['recipient'].is_seller:
            chat, created = Chat.objects.get_or_create(seller=self.request.user, buyer=serializer.validated_data['recipient'])
        elif not self.request.user.is_seller and serializer.validated_data['recipient'].is_seller:
            chat, created = Chat.objects.get_or_create(buyer=self.request.user, seller=serializer.validated_data['recipient'])
        else:
            return Response('No access')
        serializer.save(sender=request.user, chat=chat)
        chat.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            serializer = MessageUpdateSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('No access')

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            instance.delete()
            return Response('Message is deleted')
        else:
            return Response('No access')


class MessageSupportViewSet(GenericViewSet):
    serializer_class = MessageGetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        chat = ChatSupport.objects.filter(user=self.request.user)
        if chat:
            queryset = MessageSupport.objects.filter(chat=chat)
        else:
            queryset = MessageSupport.objects.filter(sender=self.request.user)
        return queryset

    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admins = CustomUser.objects.filter(is_superuser=True)
        chat, created = Chat.objects.get_or_create(user=self.request.user)
        if created:
            chat.admin.add(*admins)
        else:
            chat.admin.add(*admins)
        serializer.save(sender=request.user, chat=chat)
        chat.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            serializer = MessageUpdateSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('No access')

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            instance.delete()
            return Response('Message is deleted')
        else:
            return Response('No access')


class SupportListApiView(ListAPIView):
    serializer_class = MessageGetSerializer
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        chats = Chat.objects.filter(admin__in=[self.request.user, ]).values_list('pk', flat=True)
        if self.kwargs['pk'] in chats:
            queryset = Message.objects.filter(chat=self.kwargs['pk']).order_by('timestamp')
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response('No access')


class SupportViewSet(GenericViewSet):
    serializer_class = MessageGetSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        chat = ChatSupport.objects.filter(admin__in=[self.request.user, ])
        if chat:
            queryset = MessageSupport.objects.filter(chat=chat)
        else:
            queryset = MessageSupport.objects.filter(sender=self.request.user)
        return queryset

    def create(self, request):
        serializer = MessageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        admins = CustomUser.objects.filter(is_superuser=True)
        chat = Chat.objects.get(admin_in=[self.request.user, ], user=serializer.validated_data['recipient'])
        chat.admin.add(*admins)
        serializer.save(sender=request.user, chat=chat)
        chat.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            serializer = MessageUpdateSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('No access')

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.sender == self.request.user:
            instance.delete()
            return Response('Message is deleted')
        else:
            return Response('No access')
