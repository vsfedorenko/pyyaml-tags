import unittest

from yaml_tags import BaseTag, TagMetaClass, register, registry, tag


class RegistryTestCase(unittest.TestCase):

    def test_register(self):
        test_tag_name = 'test_register'

        class TestTag(BaseTag):
            tag_name = test_tag_name

            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        register(TestTag)

        self.assertIn(test_tag_name, registry().keys())
        self.assertEqual(registry()[test_tag_name], TestTag)

    def test_tag_decorator(self):
        test_tag_name = 'test_tag_decorator'

        @tag(name=test_tag_name)
        class TestTag(BaseTag):
            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        self.assertIn(test_tag_name, registry().keys())
        self.assertEqual(registry()[test_tag_name], TestTag)

    def test_tag_metaclass(self):
        test_tag_name = 'test_tag_metaclass'

        class TestTag(BaseTag):
            tag_name = test_tag_name

            __metaclass__ = TagMetaClass

            @classmethod
            def from_yaml(cls, *args, **kwargs):
                pass

        self.assertIn(test_tag_name, registry().keys())
        self.assertEqual(registry()[test_tag_name], TestTag)

    def test_register_base_tag_inheritance(self):
        class TestTag(object):
            tag_name = 'test_register_base_tag_inheritance'

            @classmethod
            def _from_yaml(cls, *args, **kwargs):
                pass

        def test_register():
            register(TestTag)

        self.assertRaises(ValueError, test_register)


if __name__ == '__main__':
    unittest.main()
