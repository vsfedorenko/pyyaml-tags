import io
import os
import unittest

import yaml
from path import Path
from yaml_tags import tag_registry


class EnvironmentTestCase(unittest.TestCase):
    cwd = Path(__file__).parent.abspath()

    def setUp(self):
        super(EnvironmentTestCase, self).setUp()

        tag_registry.require('env')

    def test_on_data(self):
        os.environ['WORLD'] = 'World'

        with io.open(self.cwd / 'data/env/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        self.assertDictEqual(data, {
            'b': 'Hello, World !'
        })


if __name__ == '__main__':
    unittest.main()
