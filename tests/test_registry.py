import unittest

from six import with_metaclass

from yaml_tags import BaseTag, TagAutoRegister, tag_registry


class RegistryTestCase(unittest.TestCase):

    def test_register(self):
        test_tag_name = 'test_register'

        class TestTag(BaseTag):
            tag_name = test_tag_name

            def _from_yaml(self, *args, **kwargs):
                pass

        tag_registry.register(TestTag)

        self.assertIn(test_tag_name, tag_registry.keys())
        self.assertEqual(tag_registry.get(test_tag_name), TestTag)

    def test_tag_decorator(self):
        test_tag_name = 'test_tag_decorator'

        @tag_registry.register(test_tag_name)
        class TestTag(BaseTag):
            def _from_yaml(self, *args, **kwargs):
                pass

        self.assertIn(test_tag_name, tag_registry.keys())
        self.assertEqual(tag_registry.get(test_tag_name), TestTag)

    def test_tag_metaclass(self):
        test_tag_name = 'test_tag_metaclass'

        class TestTag(with_metaclass(TagAutoRegister(), BaseTag)):
            tag_name = test_tag_name

            def _from_yaml(self, *args, **kwargs):
                pass

        self.assertIn(test_tag_name, tag_registry.keys())
        self.assertEqual(tag_registry.get(test_tag_name), TestTag)

    def test_register_base_tag_inheritance(self):
        class TestTag(object):
            tag_name = 'test_register_base_tag_inheritance'

            def _from_yaml(self, *args, **kwargs):
                pass

        def test_register():
            tag_registry.register(TestTag)

        self.assertRaises(ValueError, test_register)

    def test_require_one(self):
        @tag_registry.register('test_require_one')
        class TestTag(BaseTag):
            def _from_yaml(self, *args, **kwargs):
                pass

        tag_registry.require('test_require_one')
        self.assertTrue(TestTag.registered)

    def test_require_comma_separated(self):
        @tag_registry.register('test_require_comma_separated_1')
        class TestTag1(BaseTag):
            def _from_yaml(self, *args, **kwargs):
                pass

        @tag_registry.register('test_require_comma_separated_2')
        class TestTag2(BaseTag):
            def _from_yaml(self, *args, **kwargs):
                pass

        tag_registry.require(
            'test_require_comma_separated_1,'
            'test_require_comma_separated_2'
        )

        self.assertTrue(TestTag1.registered)
        self.assertTrue(TestTag2.registered)

    def test_require_list(self):
        @tag_registry.register('test_require_list_1')
        class TestTag1(BaseTag):
            def _from_yaml(self, *args, **kwargs):
                pass

        @tag_registry.register('test_require_list_2')
        class TestTag2(BaseTag):
            def from_yaml(self, *args, **kwargs):
                pass

        tag_registry.require([
            'test_require_list_1', 'test_require_list_2'
        ])

        self.assertTrue(TestTag1.registered)
        self.assertTrue(TestTag2.registered)

    def test_require_all(self):
        @tag_registry.register('test_require_all_1')
        class TestTag1(BaseTag):
            def _from_yaml(self, *args, **kwargs):
                pass

        @tag_registry.register('test_require_all_2')
        class TestTag2(BaseTag):
            def from_yaml(self, *args, **kwargs):
                pass

        tag_registry.require()

        self.assertTrue(TestTag1.registered)
        self.assertTrue(TestTag2.registered)

if __name__ == '__main__':
    unittest.main()
