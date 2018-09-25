# coding: utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from . import tags
from .base import BaseTag
from .registry import TagAutoRegister, tag_registry

__all__ = (BaseTag, tag_registry, TagAutoRegister)
