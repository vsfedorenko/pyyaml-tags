# coding: utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from abc import ABCMeta
from collections import OrderedDict
from inspect import isabstract as is_abstract, isclass as is_class

import six
import yaml

from .base import BaseTag


class TagRegistry(object):

    def __init__(self):
        super(TagRegistry, self).__init__()
        self._registry = OrderedDict()

    def keys(self):
        return self._registry.keys()

    def get(self, key, default=None):
        return self._registry.get(key, default)

    def register(self, key):
        if is_class(key):
            if not key.tag_name:
                raise ValueError(
                    "Unable to register tag: unable to determine "
                    "name neither from @tag(name=...) decorator "
                    "nor from tag_name = '...' class attribute"
                )
            return self._register(key.tag_name, key)

        def _decorator(cls):
            if cls.tag_name:
                raise ValueError(
                    "Names conflict: @tag(name='{}') overrides class "
                    "tag_name = '{}' attribute".format(key, cls.tag_name)
                )
            cls.tag_name = key

            return self._register(key, cls)

        return _decorator

    def _register(self, name, cls):
        if not issubclass(cls, BaseTag):
            raise ValueError(
                "Tag class '{}' must inherit BaseTag class".format(cls)
            )

        self._registry[name] = cls
        return cls

    def require(self, tags='__all__', *args):
        tags_names = []

        if args and len(args) > 0:
            tags_names.extend(args)

        if isinstance(tags, six.string_types):
            if tags == '__all__':
                tags_names.extend(self._registry.keys())
            else:
                tags_names.extend(tags.split(','))
        elif type(tags) == list:
            tags_names.extend(tags)

        for tag_name in tags_names:
            if tag_name not in self._registry.keys():
                raise ValueError(
                    "Tag '{}' is not registered. "
                    "Available tags: {}".format(
                        tag_name, self._registry.keys()
                    )
                )

            self.__require_tag(tag_name)

    def __require_tag(self, tag_name):
        tag_cls = self._registry.get(tag_name)

        if tag_cls.registered:
            return True

        tag_instance = tag_cls()

        yaml.add_implicit_resolver(
            tag_instance.yaml_tag(), tag_instance.yaml_pattern())
        yaml.add_constructor(tag_instance.yaml_tag(),
                             tag_instance.from_yaml)
        yaml.add_representer(tag_cls, tag_instance.to_yaml)

        tag_cls.registered = True
        return True


# noinspection PyPep8Naming
def TagAutoRegister(base_type=ABCMeta):
    class _metaclass(base_type):
        def __init__(self, cls_name, bases, attrs):
            super(_metaclass, self) \
                .__init__(cls_name, bases, attrs)

            if not is_abstract(self):
                tag_registry.register(self)

        def __new__(mcls, name, bases, namespace):
            cls_instance = super(_metaclass, mcls) \
                .__new__(mcls, name, bases, namespace)
            return cls_instance

    return _metaclass


tag_registry = TagRegistry()

__all__ = (tag_registry, TagAutoRegister)
