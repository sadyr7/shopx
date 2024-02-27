from rest_framework.response import Response
from .serializers import ProductSerializer, RecallSerializer,DiscountSerializer
from .models import Product, Recall, Like,Discount
from .filters import CustomFilter
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from user_profiles.models import CustomUser
from datetime import datetime
from .tasks import send_push_notification,send_push_notification_recall

class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsSeller, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all().annotate(rating=Avg("recall__rating"), likes=Count('like'))
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CustomFilter
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price"]


# Представление для получения деталей, обновления и удаления продукта
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().annotate(rating=Avg("recall__rating"), likes=Count('like'))
    serializer_class = ProductSerializer
    # permission_classes = [IsSeller, ]


class RecallListApiView(ListAPIView):
    serializer_class = RecallSerializer

    def get_queryset(self):
        queryset = Recall.objects.filter(product=self.kwargs['pk'])
        return queryset


class RecallViewSet(GenericViewSet):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer
    # permission_classes = [IsBuyer, ]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        product = serializer.validated_data['product']
        rating = serializer.validated_data['rating']
        text = serializer.validated_data['text']    
        print(request.user)
        
        title = f"Отзыв от {request.user.username} {datetime.utcnow()}\n{rating}\n{text}"
        
        whom = product.user.device_token
        
        send_push_notification_recall.delay(title, whom)
        
        return Response('Отзыв был отправлен продавцу')
    
    
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object()
        if instance.user == self.request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=None)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        if instance.user == self.request.user:
            instance.delete()
            return Response('Recall is deleted')


class LikeView(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsBuyer, ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        like = Like.objects.filter(user=self.request.user, product=instance)
        if like:
            return Response("Like was already created")
        else:
            Like.objects.create(user=self.request.user, product=instance)
            return Response("Like created")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        like = Like.objects.filter(user=self.request.user, product=instance)
        if like:
            like.delete()
            return Response("Like is deleted")
        else:
            return Response("No Like")


class DiscountListView(generics.ListCreateAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

    def post(self, request, *args, **kwargs):
        print(request.user.username)
        return super().post(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        id = instance.id
        users_with_tokens = CustomUser.objects.exclude(device_token=None)

        all_tokens = list(users_with_tokens.values_list('device_token', flat=True))

        title = f"большая скидка в магазине {instance.product.user.market_name} {datetime.utcnow()}"
        send_push_notification.delay(id, title, all_tokens)
        
    

class DiscountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer