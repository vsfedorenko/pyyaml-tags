import io
import unittest

import yaml

from yaml_tags import require as yaml_require_tags


class TimeTestCase(unittest.TestCase):

    def setUp(self):
        super(TimeTestCase, self).setUp()

        yaml_require_tags('time_now')

    def test_on_data(self):
        with io.open('data/time/now/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)

        timestamp = data['b']
        self.assertIsNotNone(timestamp)
        self.assertRegexpMatches(timestamp, r'[\d]+')

        date = data['c']
        self.assertIsNotNone(date)
        self.assertRegexpMatches(
            date, r'[\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}'
        )


if __name__ == '__main__':
    unittest.main()
