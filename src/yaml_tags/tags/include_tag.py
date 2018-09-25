# coding: utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import collections
import io
import os
import re
import sys
from glob import iglob

import six
import yaml
from six import with_metaclass

from ..base import BaseTag
from ..registry import TagAutoRegister


class IncludeTag(with_metaclass(TagAutoRegister(), BaseTag)):
    tag_name = 'include'

    wildcards_regex = re.compile(r'^.*(\*|\?|\[!?.+\]).*$')

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

        # Python 3 iterator fix
        if not isinstance(yaml_data, list):
            yaml_data = list(yaml_data)

        if all(isinstance(el, list) for el in yaml_data):
            return [el for sublist in yaml_data for el in sublist]

        if all(isinstance(el, dict) for el in yaml_data):
            result_dict = collections.defaultdict()
            for d in yaml_data:
                for k, v in six.iteritems(d):
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


__all__ = (IncludeTag,)
