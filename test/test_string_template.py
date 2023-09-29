from ygpt.utils.string_template import StringTemplate
from unittest import TestCase


class TestStringTemplate(TestCase):
    def test_format(self):
        s = StringTemplate('Hello {name}')
        res = s.format(name='world')
        self.assertEqual(res, 'Hello world')

    def test_multiple_format(self):
        s = StringTemplate('Hello {name} {sign}')
        res = s.format(name='world')
        self.assertEqual(res, 'Hello world {sign}')
        res = res.format(sign='!')
        self.assertEqual(res, 'Hello world !')

    def test_save_no_state(self):
        s = StringTemplate('Hello {name} {sign}')
        res = s.format(name='world')
        self.assertEqual(s, 'Hello {name} {sign}')

    def test_assert_wrong_key(self):
        s = StringTemplate('Hello {name}')
        with self.assertRaises(KeyError):
            s.format(wrong_key='world')

    def test_many_keys(self):
        s = StringTemplate('Hello {name} {name}')
        res = s.format(name='world')
        self.assertEqual(res, 'Hello world world')
