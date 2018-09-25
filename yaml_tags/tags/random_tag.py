import string
import sys
from random import choice, randint, random

from ..base import BaseTag
from ..meta import TagMetaClass


class RandomIntTag(BaseTag):
    tag_name = 'random_int'

    __metaclass__ = TagMetaClass

    def __new__(cls):
        return super(RandomIntTag, cls).__new__(cls)

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   a=0, b=None,
                   *args, **kwargs):
        if not b:
            b = sys.maxint

        rand = randint(a, b)

        if _prefix or _suffix:
            return _prefix + str(rand) + _suffix

        return rand


class RandomFloatTag(BaseTag):
    tag_name = 'random_float'

    __metaclass__ = TagMetaClass

    def __new__(cls):
        return super(RandomFloatTag, cls).__new__(cls)

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   *args, **kwargs):
        rand = random()

        if _prefix or _suffix:
            return _prefix + str(rand) + _suffix

        return rand


class RandomStrTag(BaseTag):
    tag_name = 'random_str'

    __metaclass__ = TagMetaClass

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
