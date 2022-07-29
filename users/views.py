from rest_framework import status, generics
from rest_framework.decorators import api_view, action  # 基于函数装饰器
from rest_framework.decorators import APIView  # 基类
from rest_framework.response import Response  # response对象
from rest_framework.permissions import AllowAny, IsAuthenticated
# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt  # 装饰器
# from rest_framework.parsers import JSONParser  # json解析器
from users.models import User
from users.serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from django.http import Http404


class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)  # 反序列化
        serializer.is_valid(raise_exception=True)  # 登录验证

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRUView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),
            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image)
            }
        }
        # serializer_data = {
        #     'username': user_data.get('username'),
        #     'email': user_data.get('email'),
        #     'profile': {
        #         'bio': user_data.get('bio'),
        #         'image': user_data.get('image')
        #     }
        # }
        # instance 使用 partial 参数来允许部分更新
        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
