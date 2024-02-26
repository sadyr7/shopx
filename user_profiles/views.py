from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken

from .services import *
from .serializers import *
from drf_spectacular.utils import extend_schema

# апи для регистрации user sellers wholeseller
class UserRegisterView(CreateUserApiView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer


class SellerRegisterView(CreateUserApiView):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerRegisterSerializer




# апи который проверяет код который был отправлен на указанный email и в ответ передает токен
class UserVerifyRegisterCode(generics.UpdateAPIView):
    serializer_class = VerifyCodeSerializer

    http_method_names = ['patch',]
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')
        return CheckCode.check_code(code=code)



class ForgetPasswordSendCodeView(generics.UpdateAPIView):
    serializer_class = SendCodeSerializer

    def put(self, request, *args, **kwargs):
        email_or_phone = request.data.get("email_or_phone")
        return ChangePassword.send_email_code(email_or_phone=email_or_phone)

        


# апи для того чтобы сттать продавцом 
class BecomeSellerView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        user.is_seller = True
        user.save()
        return Response("Вы успешно стали продавцом", status=status.HTTP_200_OK)



# если user забыл пароль при входе

class ForgetPasswordView(generics.UpdateAPIView):
    serializer_class = ForgetPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]


    def update(self, request, *args, **kwargs):
        
        result = ChangePassword.change_password_on_reset(self=self,request=request)

        if result == "success":
            return Response("Пароль успешно изменен", status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)



# апи менят пароль в профиле 
class UserResetPasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
            result = ChangePassword.change_password_on_profile(request=request)

            if result == "success":
                return Response("Пароль успешно изменен", status=status.HTTP_200_OK)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)




class ListProfileApi(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer



class UpdateUserProfileApi(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'id'

class DetailUserProfileApi(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'



class SellerListApiview(generics.ListAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]


class SellerUpdateProfileApi(generics.UpdateAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]
    lookup_field = 'id'


class SellerDetailProfileApi(generics.RetrieveAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    lookup_field = 'id'



class MarketListAPIView(generics.ListAPIView):
    queryset = SellerProfile.objects.prefetch_related('products').all()
    serializer_class = MarketSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10



class LogoutView(generics.GenericAPIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            # Также инвалидируем Access Token'ы пользователя
            OutstandingToken.objects.filter(user=request.user).delete()
            
            # Удаление device_token у пользователя
            user = request.user
            user.device_token = None
            user.save()

            return Response("Successfully logged out.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
