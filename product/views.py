from rest_framework.response import Response
from rest_framework import generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ProductSerializer, RecallSerializer
from .models import Product, Recall, Like
from .filters import CustomFilter
from datetime import datetime
from rest_framework import permissions
from .tasks import send_push_notification_recall
from Shopx.settings import REDIS_TIMEOUT
from django.core.cache import cache
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny



class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny, ]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ProductListApiView(ListAPIView):
    queryset = Product.objects.all().annotate(rating=Avg("recall__rating"), likes=Count('like'))
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CustomFilter
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price"]

    def HistorySearch(self):
        pass

    @action(
        methods=['get'],
        detail=False,
        url_path='profile',
        serializer_class=None,
        permission_classes=[AllowAny]
    )


    # def get(self, request):
    #     recent_words = cache.get('recent_words')
    #     if not recent_words:
    #         recent_words = Product.objects.order_by('-created_at')[:10]  
    #         cache.set('recent_words', recent_words, REDIS_TIMEOUT)
    #     serializer = ProductSerializer(recent_words, many=True)
    #     return Response(serializer.data)



# Представление для получения деталей, обновления и удаления продукта
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().annotate(rating=Avg("recall__rating"), likes=Count('like'))
    serializer_class = ProductSerializer
    # permission_classes = [IsSeller, ]

    def perform_update(self, serializer):
        instance = serializer.instance
        instance.price = serializer.apply_discount_to_price(instance.price, serializer.validated_data.get('discount', 0))
        instance.save()


# Представление для получения деталей, обновления и удаления продукта

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
