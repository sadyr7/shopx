from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view()),

    path('seller/register/',SellerRegisterView.as_view(), name='seller-register'),

    path('refresh-token/', TokenRefreshView.as_view()),
    path('send-code-to-email/', ForgetPasswordSendCodeView.as_view(), name='send_password_reset_code'),
    path('verify-register-code/', UserVerifyRegisterCode.as_view(), name='verify_register_code'),
    path('forget-password/reset/', ForgetPasswordView.as_view(), name='reset_password'),
    path('become-seller/', BecomeSellerView.as_view(), name='become_seller'),
    path('reset-password-profile/', UserResetPasswordView.as_view(), name='reset_password'),


    path('profiles/', ListProfileApi.as_view(), name=''),
    path('profile/<int:id>/', DetailUserProfileApi.as_view(), name=''),
    path('profile/update/<int:id>/', UpdateUserProfileApi.as_view(), name=''),

    path('seller-profiles/',SellerListApiview.as_view()),
    path('seller-profile/<int:id>/', DetailUserProfileApi.as_view(), name=''),
    path('seller-profile/update/<int:id>/', UpdateUserProfileApi.as_view(), name=''),

    path('market/', MarketListAPIView.as_view(), name=''),
    #path('logout/', LogoutView.as_view(), name=''),
]