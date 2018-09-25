import io
import os
import unittest

import yaml

from yaml_tags import require as yaml_require_tags


class EnvironmentTestCase(unittest.TestCase):

    def setUp(self):
        super(EnvironmentTestCase, self).setUp()

        yaml_require_tags('env')

    def test_on_data(self):
        os.environ['WORLD'] = 'World'

        with io.open('data/env/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        self.assertDictEqual(data, {
            'b': 'Hello, World !'
        })


if __name__ == '__main__':
    unittest.main()
