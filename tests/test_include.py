import io
import unittest

import yaml

from yaml_tags import require as yaml_require_tags


class IncludeTestCase(unittest.TestCase):

    def setUp(self):
        super(IncludeTestCase, self).setUp()

        yaml_require_tags('include')

    def test_on_data(self):
        with io.open('data/include/a.yml') as fh:
            data = yaml.load(fh)
        self.assertIsNotNone(data)
        self.assertDictEqual(data, {
            'b': ['1', 2, '3'],
            'c': {'c1': '2', 'c2': '2', 'c3': 3},
            'd': {'d1': 1, 'd2': 2},
            'e': {'e1': 1, 'e2': [1, 2]},
            'f': [1, {'f1': 1, 'f2': 2}]
        })


if __name__ == '__main__':
    unittest.main()
