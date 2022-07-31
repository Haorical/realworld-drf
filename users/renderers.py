from core.renderers import MyJSONRenderer


class UserJSONRenderer(MyJSONRenderer):
    object_label = 'user'
    pagination_object_label = 'users'
    pagination_object_count = 'usersCount'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        token = data.get('token', None)
        return super(UserJSONRenderer, self).render(data)
