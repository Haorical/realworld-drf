from django.urls import path, include
from articles.views import (
    ArticleViewSet, ArticlesFavoriteAPIView, ArticlesFeedAPIView,
    CommentsListCreateAPIView, CommentsDestroyAPIView, TagListAPIView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('articles', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),  # list/
    path('articles/feed', ArticlesFeedAPIView.as_view()),  # feed
    path('articles/<str:article_slug>',ArticleViewSet.as_view),  # get create update article
    path('articles/<str:article_slug>/comments', CommentsListCreateAPIView.as_view()),  # add get comments
    path('articles/<str:article_slug>/comments/<int:comment_pk>', CommentsDestroyAPIView.as_view()),  # delete comments
    path('articles/<str:article_slug>/favorite', ArticlesFavoriteAPIView.as_view()),  # (un)favorite article
    path('tags', TagListAPIView.as_view())  # list tags
]
