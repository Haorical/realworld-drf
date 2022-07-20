from rest_framework import serializers
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()  # 可以在返回数据之前,对数据进行一些更改
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'bio', 'image', 'following']
        read_only_fields = ['username']

    def get_image(self, obj):
        if obj.image:
            return self.image
        return 'https://img-home.csdnimg.cn/images/20201124032511.png'

    def get_following(self, obj):
        request = self.context.get('request', None)
        follower = request.user.profile
        followee = obj

        return follower.is_following(followee)
