from datetime import datetime
from time import time

from ..base import BaseTag
from ..meta import TagMetaClass


class TimeNowTag(BaseTag):
    tag_name = 'time_now'

    __metaclass__ = TagMetaClass

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   timestamp=True, fmt="%Y-%m-%d %H:%M:%S",
                   *args, **kwargs):
        if timestamp:
            return _prefix + str(int(time())) + _suffix

        now = datetime.now()
        return _prefix + now.strftime(fmt) + _suffix
