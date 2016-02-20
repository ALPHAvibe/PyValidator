import unittest
import os
import sys
# backup one directory to import pyvalidator from a different folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_validator import *


class ValueValidatorTest(unittest.TestCase):

    def test_object_validator(self):
        foo = {
            'foo1': 'bar',
            'foo2': {
                'inner_foo': 'inner_bar'
            }
        }

        nested_foo_validator = PyValidator()\
            .stop_on_first_error()\
            .rules_for('inner_foo', lambda o: o['inner_foo'])\
                .not_none()\
                .is_string()

        response = PyValidator()\
            .stop_on_first_error()\
            .rules_for('foo1', lambda o: o['foo1'])\
                .not_none()\
                .is_string()\
            .rules_for('foo2', lambda o: o['foo2'])\
                .set_validator(nested_foo_validator)\
            .validate(foo)

        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_list_object_validator(self):
        foo = {
            'foo1': 'bar',
            'foo2': [
                {
                    'inner_foo': 'inner_bar1'
                },
                {
                    'inner_foo': 'inner_bar2'
                }
            ]
        }

        nested_foo_validator = PyValidator()\
            .stop_on_first_error()\
            .rules_for('inner_foo', lambda o: o['inner_foo'])\
                .not_none()\
                .is_string()

        response = PyValidator()\
            .stop_on_first_error()\
            .rules_for('foo1', lambda o: o['foo1'])\
                .not_none()\
                .is_string()\
            .rules_for('foo2', lambda o: o['foo2'])\
                .is_length_equals(2)\
                .set_validator(nested_foo_validator)\
            .validate(foo)

        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

if __name__ == '__main__':
    unittest.main(exit=False)
