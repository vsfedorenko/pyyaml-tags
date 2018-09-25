import collections
import io
import os
import re
import sys
from glob import iglob

import yaml

from ..base import BaseTag
from ..meta import TagMetaClass


class IncludeTag(BaseTag):
    tag_name = 'include'

    wildcards_regex = re.compile(r'^.*(\*|\?|\[!?.+\]).*$')

    __metaclass__ = TagMetaClass

    def __new__(cls):
        instance = super(IncludeTag, cls).__new__(cls)

        instance.glob_func = lambda p, r: iglob(p, recursive=r) \
            if sys.version_info >= (3, 5) \
            else iglob(p)

        return instance

    def _from_yaml(self, _loader, _work_dir, _prefix, _suffix,
                   path=None, recursive=False, encoding='utf-8',
                   *args, **kwargs):

        if not path:
            raise ValueError("No path were specified")

        path = _work_dir / path

        yaml_data = map(
            lambda path: self._include_path(_loader, path, encoding),
            self._list_files(path, recursive)
        )

        if all(isinstance(el, list) for el in yaml_data):
            return [el for sublist in yaml_data for el in sublist]

        if all(isinstance(el, dict) for el in yaml_data):
            result_dict = collections.defaultdict()
            for d in yaml_data:
                for k, v in d.iteritems():  # d.items() in Python 3+
                    result_dict[k] = v
            return dict(result_dict)

        return yaml_data

    def _list_files(self, path, recursive):
        if self.wildcards_regex.match(path):
            return self.glob_func(path, recursive)
        else:
            return iter([path])

    def _include_path(self, loader, path, encoding):
        if not os.path.isfile(path):
            raise ValueError("Path '{}' is not a file".format(path))

        with io.open(path, encoding=encoding) as fh:
            return yaml.load(fh, type(loader))
