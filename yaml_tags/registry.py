import yaml

from .base import BaseTag

_registry = {}


def tag(name=None):
    def decorator(cls):
        if name:
            if cls.tag_name:
                raise ValueError(
                    "Names conflict: @tag(name='{}') overrides class "
                    "tag_name = '{}' attribute".format(name, cls.tag_name)
                )
            cls.tag_name = name
        else:
            if not cls.tag_name:
                raise ValueError(
                    "Unable to register tag: unable to determine "
                    "name neither from @tag(name=...) decorator "
                    "nor from tag_name = '...' class attribute"
                )

        register(cls)

        return cls

    return decorator


def register(cls):
    if not issubclass(cls, BaseTag):
        raise ValueError("Tag class must inherit BaseTag class")

    _registry[cls.tag_name] = cls


def registry():
    return dict(_registry)


def require(tags='__all__', *args):
    tags_names = []

    if args and len(args) > 0:
        tags_names.extend(args)

    if type(tags) == str:
        if tags == '__all__':
            tags_names.extend(_registry.keys())
        else:
            tags_names.extend(tags.split(','))
    elif type(tags) == list:
        tags_names.extend(tags)

    for tag_name in tags_names:
        tag_cls = _registry[tag_name]

        tag_instance = tag_cls()

        if tag_instance.registered:
            continue

        yaml.add_implicit_resolver(
            tag_instance.yaml_tag(), tag_instance.yaml_pattern())
        yaml.add_constructor(tag_instance.yaml_tag(), tag_instance.from_yaml)
        yaml.add_representer(tag_cls, tag_instance.to_yaml)

        tag_cls.registered = True
