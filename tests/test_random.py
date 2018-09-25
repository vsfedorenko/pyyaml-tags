import io
import unittest

import yaml

from yaml_tags import require as yaml_require_tags


class RandomTestCase(unittest.TestCase):
    def setUp(self):
        super(RandomTestCase, self).setUp()

        yaml_require_tags('random_int', 'random_float', 'random_str')

    def test_int_on_data(self):
        with io.open('data/random/int/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        rand_number = data['b']

        self.assertIsNotNone(rand_number)
        self.assertRegexpMatches(str(rand_number), r'[\d]+')

    def test_float_on_data(self):
        with io.open('data/random/float/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        rand_number = data['b']

        self.assertIsNotNone(rand_number)
        self.assertRegexpMatches(str(rand_number), r'[\d]+.[\d]+')

    def test_str_on_data(self):
        with io.open('data/random/str/a.yml') as fh:
            data = yaml.load(fh)

        self.assertIsNotNone(data)
        rand_str_10_mixed = data['b']
        self.assertIsNotNone(rand_str_10_mixed)
        self.assertRegexpMatches(rand_str_10_mixed, r'[a-zA-Z0-9]{10}')

        rand_str_100_upper = data['c']
        self.assertIsNotNone(rand_str_100_upper)
        self.assertRegexpMatches(rand_str_100_upper, r'[A-Z0-9]{100}')

        rand_str_50_lower = data['d']
        self.assertIsNotNone(rand_str_50_lower)
        self.assertRegexpMatches(rand_str_50_lower, r'[a-z0-9]{50}')


if __name__ == '__main__':
    unittest.main()
