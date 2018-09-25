from .registry import register


# noinspection PyMethodParameters
class TagMetaClass(type):

    def __init__(self, *args, **kwargs):
        super(TagMetaClass, self).__init__(*args, **kwargs)

    def __new__(cls, cls_name, bases, attrs):
        cls_instance = super(TagMetaClass, cls) \
            .__new__(cls, cls_name, bases, attrs)

        tag_name = attrs.get('tag_name', None)
        if not tag_name:
            raise ValueError('tag_name attribute can\'t be None')

        register(cls_instance)

        return cls_instance
