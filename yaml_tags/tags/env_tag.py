import os

from ..base import BaseTag
from ..meta import TagMetaClass


class EnvTag(BaseTag):
    tag_name = 'env'

    __metaclass__ = TagMetaClass

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
