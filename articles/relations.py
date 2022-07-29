from rest_framework import serializers

from articles.models import Tag


# 序列化：抽象的模型对象 转换成 直观的字典 json 设置many，可以传一个query_set,序列化成一组json
# 反序列化： 字典转为模型对象
class TagRelatedField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()

    def to_internal_value(self, data):  # 改变反序列化输出
        tag, created = Tag.objects.get_or_create(tag=data, slug=data.lower())
        return tag

    def to_representation(self, value):  # 改变序列化输出
        return value.tag
