import unittest
import os
import sys
# backup one directory to import pyvalidator from a different folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_validator import *


class ControlFlowTest(unittest.TestCase):

    def test_global_stop_on_first_error_works(self):
        response = PyValidator()\
            .stop_on_first_error()\
            .rules_for('foo1', lambda o: o['foo1'])\
                .not_none()\
                .is_int()\
            .rules_for('foo2', lambda o: o['foo2'])\
                .not_none()\
                .is_int()\
            .validate({'foo1': 'bar', 'foo2': 'bar'})

        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 2)

    def test_stop_on_first_error__works(self):
        response = PyValidator()\
            .rules_for('foo1', lambda o: o['foo1'])\
                .stop_on_first_error()\
                .not_none()\
                .is_int()\
            .rules_for('foo2', lambda o: o['foo2'])\
                .not_none()\
                .is_int()\
            .validate({'foo1': 'bar', 'foo2': None})

        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 3)

    def test_stop_on_error__works(self):
        response = PyValidator()\
            .rules_for('foo1', lambda o: o['foo1'])\
                .not_none()\
                .is_int()\
            .rules_for('foo2', lambda o: o['foo2'])\
                .not_none()\
                .is_string()\
                .is_between(5, 10)\
                    .stop_on_error()\
                .is_equals(16)\
            .validate({'foo1': 15, 'foo2': 20})

        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 2)

if __name__ == '__main__':
    unittest.main(exit=False)
