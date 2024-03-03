from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recall', RecallViewSet, basename='recall')

urlpatterns = [

    path("product/list/", ProductListApiView.as_view(), name="product-list"),
    path('product/create/', ProductCreateApiView.as_view(), name='product-create'),
    # path('update/product/<int:id>/', ProductUpdateApiView.as_view()),

    path("like/<int:pk>/", LikeView.as_view(), name="like"),
    path('recall-list/<int:pk>/', RecallListApiView.as_view(), name='recall-list'),
    path('', include(router.urls)),
    # path('viewed-products/', ViewedProductListCreate.as_view(), name='viewed-product-list'),
    # path('viewed-products/<int:pk>/', ViewedProductDetail.as_view(), name='viewed-product-detail'),
]


