from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from profiles.serializers import ProfileSerializer
from profiles.models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)  # 仅用于反序列化输入
    token = serializers.CharField(max_length=255, read_only=True)  # 仅用于序列化输出

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        user = User.objects.creat_user(**validated_data)
        profile = Profile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):  # 没有继承model
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    # 登录验证
    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        if email is None:
            raise serializers.ValidationError("no email")
        if password is None:
            raise serializers.ValidationError('no password')
        user = authenticate(username=email, password=password)  # 检查账号密码是否匹配
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)
    profile = ProfileSerializer(write_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        model = User  # 序列化类
        fields = ['email', 'bio', 'image', 'username', 'password', 'token', 'profile']  # 类字段 序列化字段
        read_only_fields = ['token']  # model中的token设置成只读字段，不需要另外定义属性

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # password有加密，不能直接设置
        profile_data = validated_data.pop('profile', {})  # profile是个类，也不能直接遍历
        for key, value in validated_data.items():
            setattr(instance, key, value)  # 用于设置属性值，该属性不一定是存在的。
        if password is None:
            instance.set_password(password)
        instance.save()
        for key, value in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()
        return instance
