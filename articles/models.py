from core.models import TimestampModel
from django.db import models


class Article(TimestampModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True, null=True)
    title = models.CharField(db_index=True, max_length=255)
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)
    tags = models.ManyToManyField(
        'articles.Tag',
        related_name='articles'
    )
    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='articles',
        null=True,
    )
    def __str__(self): return self.slug


class Comment(TimestampModel):
    body = models.TextField()
    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
        related_name='comments'
    )


class Tag(TimestampModel):
    tag = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, db_index=True)
