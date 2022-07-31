from core.renderers import MyJSONRenderer


class ArticleJSONRenderer(MyJSONRenderer):
    object_label = 'article'
    pagination_object_label = 'articles'
    pagination_object_count = 'articlesCount'


class CommentJOSNRenderer(MyJSONRenderer):
    object_label = 'comment'
    pagination_object_label = 'comments'
    pagination_object_count = 'commentCount'
