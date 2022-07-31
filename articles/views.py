from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Comment, Tag
from articles.serializers import ArticleSerializer, CommentSerializer, TagSerializer
from articles.renderers import ArticleJSONRenderer, CommentJOSNRenderer


class ArticleViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author', 'author__user') # 外键和外键的外键的字段名全获取了
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    renderer_classes = [ArticleJSONRenderer]

    def get_queryset(self):
        queryset = self.queryset

        author = self.request.query_params.get('author', None)  # 获取url中的params
        if author is not None:
            queryset = queryset.filter(author__user__username=author)  # 直接用filter过滤

        tag = self.request.query_params.get('tag', None)
        if tag is not None:
            queryset = queryset.filter(tags__tag=tag)

        favorited_by = self.request.query_params.get('favorited', None)
        if favorited_by is not None:
            queryset = queryset.filter(
                favorited_by__user__username=favorited_by
            )

        return queryset

    def create(self, request):
        serializer_context = {
            'author': request.user.profile, # 传的author是个profile类型对象
            'request': request
        }
        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            data=serializer_data, context=serializer_context
        )  # 反序列化
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        serializer_context = {'request': request}
        page = self.paginate_queryset(self.get_queryset())  # 分页 且 过滤 调用的有过滤的get_queryset而不是queryset

        serializer = self.serializer_class(
            page,
            context=serializer_context,
            many=True
        )

        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, slug):
        serializer_context = {'request': request}

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer = self.serializer_class(
            serializer_instance,
            context=serializer_context
        )  # 序列化

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, slug):
        serializer_context = {'request': request}  # 上下文

        try:
            serializer_instance = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')

        serializer_data = request.data.get('article', {})

        serializer = self.serializer_class(
            serializer_instance,  # 序列化 对象
            context=serializer_context,
            data=serializer_data,  # 反序列化 data参数
            partial=True  # 部分更新
        )  # 序列化+反序列化 update
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsListCreateAPIView(generics.ListCreateAPIView):
    lookup_field = 'article__slug'
    lookup_url_kwarg = 'article_slug'
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.select_related(
        'article', 'article__author', 'article__author__user',
        'author', 'author__user'
    )
    serializer_class = CommentSerializer
    renderer_classes = [CommentJOSNRenderer]

    def filter_queryset(self, queryset):
        filters = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        # filters = {'article__slug': kwargs['article_slug']}
        # kwargs就是查询的参数字典

        return queryset.filter(**filters)  # article__slug=article_slug

    def create(self, request, article_slug=None):
        data = request.data.get('comment', {})
        context = {'author': request.user.profile}
        # print(request.user.username)
        try:
            context['article'] = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug does not exist.')
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentsDestroyAPIView(generics.DestroyAPIView):
    lookup_url_kwarg = 'comment_pk'
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()  # 先获取所有再get或filter
    renderer_classes = [CommentJOSNRenderer]

    def destroy(self, request, article_slug=None, comment_pk=None):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound('A comment with this ID does not exist.')

        comment.delete()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArticlesFavoriteAPIView(APIView):  # 继承的低级版本写 delete 和 post方法
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    renderer_classes = [ArticleJSONRenderer]

    def delete(self, request, article_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        profile.unfavorite(article)

        serializer = self.serializer_class(article, context=serializer_context)  # 序列化

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_slug=None):
        profile = self.request.user.profile
        serializer_context = {'request': request}

        try:
            article = Article.objects.get(slug=article_slug)
        except Article.DoesNotExist:
            raise NotFound('An article with this slug was not found.')

        profile.favorite(article)

        serializer = self.serializer_class(article, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer

    def list(self, request):
        serializer_data = self.get_queryset()  # 直接所有的queryset
        serializer = self.serializer_class(serializer_data, many=True)

        return Response({
            'tags': serializer.data  # many返回一个数组
        }, status=status.HTTP_200_OK)


class ArticlesFeedAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    renderer_classes = [ArticleJSONRenderer]

    def get_queryset(self):
        return Article.objects.filter(
            author__in=self.request.user.profile.follows.all()
            # 查询author是否在user follow的集合中
        )

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            page, context=serializer_context, many=True
        )

        return self.get_paginated_response(serializer.data)