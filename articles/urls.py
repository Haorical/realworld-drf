from django.urls import path
from articles.views import (
    ArticleViewSet, ArticlesFavoriteAPIView, ArticlesFeedAPIView,
    CommentsListCreateAPIView, CommentsDestroyAPIView, TagListAPIView
)


urlpatterns = [
    path('articles', ArticleViewSet.as_view),  # list/
    path('articles/feed', ArticlesFeedAPIView.as_view()),  # feed
    path('articles/<str:slug>',ArticleViewSet.as_view),  # get create update article
    path('articles/<str:slug>/comments', CommentsListCreateAPIView.as_view()),  # add get comments
    path('articles/<str:slug>/comments/<int:id>', CommentsDestroyAPIView.as_view()),  # delete comments
    path('articles/<str:slug>/favorite', ArticlesFavoriteAPIView.as_view()),  # (un)favorite article
    path('articles/tags', TagListAPIView.as_view())  # list tags
]
