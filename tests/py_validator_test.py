import unittest
import os
import sys
# backup one directory to import pyvalidator from a different folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_validator import *


class PersonFoo(object):
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.age = ''
        self.gender = None


class PyValidatorTest(unittest.TestCase):

    def test_is_string_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_string().validate('foo')
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_string_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_string().validate(1)
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_int_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_int().validate(1)
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_int_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_int().validate('foo')
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_long_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_long().validate(0x7fffffff)
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_long_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_long().validate('foo')
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_float_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_float().validate(1.3)
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_float_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_float().validate('foo')
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_greater_than_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_greater_than(4).validate(5)
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_greater_than_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_greater_than(6).validate(5)
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_less_than_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_less_than(6).validate(5)
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_less_than_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_less_than(4).validate(5)
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_between_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_between(4, 6).validate(5)
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_between_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_between(4, 6).validate(8)
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_equals_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_equals(4).validate(4)
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_equals_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_equals(4).validate(8)
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_length_equals_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_length_equals(3).validate('foo')
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_length_equals_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_length_equals(4).validate('foofoo')
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_is_length_between_true(self):
        response = PyValidator().rules_for('value', lambda o: o).is_length_between(1, 6).validate('foofoo')
        self.assertTrue(response.is_valid)
        self.assertEqual(len(response.errors), 0)

    def test_is_length_between_false(self):
        response = PyValidator().rules_for('value', lambda o: o).is_length_between(1, 6).validate('foofoofoo')
        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

if __name__ == '__main__':
    unittest.main(exit=False)
