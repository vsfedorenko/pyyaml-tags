import unittest

from yaml_tags import BaseTag, IncludeTag, require as yaml_require_tags, tag


class RequireTestCase(unittest.TestCase):

    def test_require_one(self):
        @tag(name='test_require_one')
        class TestTag(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        yaml_require_tags('test_require_one')
        self.assertTrue(IncludeTag.registered)

    def test_require_comma_separated(self):
        @tag(name='test_require_comma_separated_1')
        class TestTag1(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        @tag(name='test_require_comma_separated_2')
        class TestTag2(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        yaml_require_tags(
            'test_require_comma_separated_1,'
            'test_require_comma_separated_2'
        )

        self.assertTrue(TestTag1.registered)
        self.assertTrue(TestTag2.registered)

    def test_require_list(self):
        @tag(name='test_require_list_1')
        class TestTag1(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        @tag(name='test_require_list_2')
        class TestTag2(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        yaml_require_tags(['test_require_list_1', 'test_require_list_2'])

        self.assertTrue(TestTag1.registered)
        self.assertTrue(TestTag2.registered)

    def test_require_all(self):
        @tag(name='test_require_all_1')
        class TestTag1(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        @tag(name='test_require_all_2')
        class TestTag2(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        yaml_require_tags()

        self.assertTrue(TestTag1.registered)
        self.assertTrue(TestTag2.registered)


if __name__ == '__main__':
    unittest.main()
