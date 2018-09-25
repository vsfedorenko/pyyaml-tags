import io
import unittest

import six
import yaml
from path import Path
from yaml_tags import tag_registry


class TimeTestCase(unittest.TestCase):
    cwd = Path(__file__).parent.abspath()

    def setUp(self):
        super(TimeTestCase, self).setUp()

        tag_registry.require('time_now')

    def test_on_data(self):
        with io.open(self.cwd / 'data/time/now/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)

        timestamp = data['b']
        self.assertIsNotNone(timestamp)
        six.assertRegex(self, timestamp, r'[\d]+')

        date = data['c']
        self.assertIsNotNone(date)
        six.assertRegex(
            self, date, r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}'
        )


if __name__ == '__main__':
    unittest.main()
