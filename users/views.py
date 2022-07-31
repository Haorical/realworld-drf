from rest_framework import status, generics
from rest_framework.decorators import APIView  # 基类
from rest_framework.response import Response  # response对象
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from users.renderers import UserJSONRenderer


class RegistrationView(APIView):
    renderer_classes = [UserJSONRenderer]
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
    renderer_classes = [UserJSONRenderer]
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)  # 反序列化
        serializer.is_valid(raise_exception=True)  # 登录验证

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRUView(generics.RetrieveUpdateAPIView):
    renderer_classes = [UserJSONRenderer]
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
            'password': user_data.get('password', None),
            'profile': {
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image)
            }
        }
        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
