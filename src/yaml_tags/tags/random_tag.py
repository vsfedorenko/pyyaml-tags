# coding: utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import string
import sys
from random import choice, randint, random

from six import with_metaclass

from ..base import BaseTag
from ..registry import TagAutoRegister


class RandomIntTag(with_metaclass(TagAutoRegister(), BaseTag)):
    tag_name = 'random_int'

    def __new__(cls):
        return super(RandomIntTag, cls).__new__(cls)

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   a=0, b=None,
                   *args, **kwargs):
        if not b:
            b = sys.maxsize

        rand = randint(a, b)

        if _prefix or _suffix:
            return _prefix + str(rand) + _suffix

        return rand


class RandomFloatTag(with_metaclass(TagAutoRegister(), BaseTag)):
    tag_name = 'random_float'

    def __new__(cls):
        return super(RandomFloatTag, cls).__new__(cls)

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   *args, **kwargs):
        rand = random()

        if _prefix or _suffix:
            return _prefix + str(rand) + _suffix

        return rand


class RandomStrTag(with_metaclass(TagAutoRegister(), BaseTag)):
    tag_name = 'random_str'

    def __new__(cls):
        return super(RandomStrTag, cls).__new__(cls)

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   length=10, uppercase=False, lowercase=False,
                   *args, **kwargs):
        rand = ''.join(
            choice(string.ascii_letters + string.digits)
            for _ in range(length)
        )

        if uppercase and lowercase:
            raise ValueError(
                "Uppercase and lowercase parameters "
                "can't be consumed both together"
            )

        if uppercase:
            rand = rand.upper()

        if lowercase:
            rand = rand.lower()

        return _prefix + rand + _suffix


__all__ = (RandomIntTag, RandomFloatTag, RandomStrTag)
