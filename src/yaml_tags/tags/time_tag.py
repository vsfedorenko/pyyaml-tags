# coding: utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from datetime import datetime
from time import time

from six import with_metaclass

from ..base import BaseTag
from ..registry import TagAutoRegister


class TimeNowTag(with_metaclass(TagAutoRegister(), BaseTag)):
    tag_name = 'time_now'

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   timestamp=True, fmt="%Y-%m-%d %H:%M:%S",
                   *args, **kwargs):
        if timestamp:
            return _prefix + str(int(time())) + _suffix

        now = datetime.now()
        return _prefix + now.strftime(fmt) + _suffix


__all__ = (TimeNowTag,)
