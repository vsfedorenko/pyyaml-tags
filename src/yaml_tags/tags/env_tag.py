# coding: utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import os

from six import with_metaclass

from ..base import BaseTag
from ..registry import TagAutoRegister


class EnvTag(with_metaclass(TagAutoRegister(), BaseTag)):
    tag_name = 'env'

    def __new__(cls):
        return super(EnvTag, cls).__new__(cls)

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   var=None,
                   *args, **kwargs):
        if not var:
            raise ValueError("No environment variable were specified")

        if not var in os.environ:
            raise ValueError(
                'Environment variable \'{}\' is not set'.format(var)
            )

        return _prefix + str(os.environ[var]) + _suffix


__all__ = (EnvTag,)
