import unittest
import os
import sys
# backup one directory to import pyvalidator from a different folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_validator import *


class ConditionalsTest(unittest.TestCase):

    def test_when_works(self):
        response = PyValidator()\
            .rules_for('foo1', lambda o: o['foo1'])\
                .not_none()\
                .is_int()\
            .when(lambda o: o['foo1'] != 'bar')\
            .rules_for('foo2', lambda o: o['foo2'])\
                .not_none()\
                .is_int()\
            .validate({'foo1': 'bar', 'foo2': 'bar'})

        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

    def test_conditional_works(self):
        response = PyValidator()\
            .rules_for('foo1', lambda o: o['foo1'])\
                .not_none()\
                .is_int()\
            .rules_for('foo2', lambda o: o['foo2'])\
                .not_none(conditional=lambda o: o['foo1'] != 'bar')\
                .is_int(conditional=lambda o: o['foo1'] != 'bar')\
            .validate({'foo1': 'bar', 'foo2': 'bar'})

        self.assertTrue(not response.is_valid)
        self.assertEqual(len(response.errors), 1)

if __name__ == '__main__':
    unittest.main(exit=False)
