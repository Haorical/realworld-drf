from django.db import models
from core.models import TimestampModel


class Profile(TimestampModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)  # 一对一模型 级联删除
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    follows = models.ManyToManyField(
        'self',  # 自连接
        related_name='followed_by',
        symmetrical=False  # 非对称 单方向关注
    )
    favorites = models.ManyToManyField(
        'articles.Article',
        related_name='favorited_by'  # 相当于article有一个profile类型的favorited_by字段
    )
    def __str__(self): return self.user.username

    def follow(self, profile): self.follows.add(profile)

    def unfollow(self, profile): self.follows.remove(profile)

    def is_following(self, profile): return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile): return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, article): self.favorites.add(article)

    def unfavorite(self, article): self.favorites.remove(article)

    def has_favorited(self, article): return self.favorites.filter(pk=article.pk).exists()

