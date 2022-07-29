from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from articles.models import Article


@receiver(pre_save, sender=Article)  # 保存之前改一下slug
def add_slug_to_article_if_not_exists(sender, instance, *args, **kwargs):
    # MAXIMUM_SLUG_LENGTH = 255

    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = '11111111'

        instance.slug = slug + unique
