from rest_framework import serializers

from articles.models import Article, Comment, Tag
from profiles.serializers import ProfileSerializer
from articles.relations import TagRelatedField


class ArticleSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()
    tagList = TagRelatedField(many=True, required=False, source='tags')
    createdAt = serializers.SerializerMethodField(method_name='get_create_time')
    updatedAt = serializers.SerializerMethodField(method_name='get_update_time')

    class Meta:
        model = Article
        fields = ['slug', 'title', 'description', 'body',
                  'tagList', 'createdAt', 'updatedAt',
                  'favorited', 'favoritesCount', 'author']

    def get_favorited(self, instance):
        request = self.context.get('request', None)  # 需要给他传上下文
        print(request)
        if request is None:
            return False
        # if not request.user.profile.is_authenticted:
        #     return False
        return request.user.profile.has_favorited(instance)

    def get_favoritesCount(self, instance):
        return instance.favorited_by.count()  # favorited_by在profile模型中声明

    # def get_TagList(self, instance):
    #     return instance.tags

    def get_create_time(self, instance):
        return instance.created_at.isoformat()

    def get_update_time(self, instance):
        return instance.updated_at.isoformat()

    def create(self, validated_data):
        author = self.context.get('author', None)
        tags = validated_data.pop('tags',[])
        article = Article.objects.create(author=author, **validated_data)
        # 传的字典会自动改成key=value的形式
        for tag in tags:
            article.tags.add(tag)
        return article


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(required=False)
    createdAt = serializers.SerializerMethodField(method_name='get_create_time')
    updatedAt = serializers.SerializerMethodField(method_name='get_update_time')

    class Meta:
        model = Comment
        fields = [
            'id',
            'createdAt',
            'updatedAt',
            'body',
            'author',
        ]

    def get_create_time(self, instance):
        return instance.created_at.isoformat()

    def get_update_time(self, instance):
        return instance.updated_at.isoformat()

    def create(self, validated_data):
        article = self.context.get('article')
        author = self.context.get('author')
        return Comment.objects.create(author=author, article=article, **validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']  # 只有一个tag字段

    def to_representation(self, obj):  # 好像没啥必要
        return obj.tag  # 改变序列化输出 即只序列化一个tag字段
