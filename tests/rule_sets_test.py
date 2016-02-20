import unittest
import os
import sys
# backup one directory to import pyvalidator from a different folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from py_validator import *


class RuleSetsTest(unittest.TestCase):

    def test_rule_sets_works(self):
        validator = PyValidator()\
            .rules_for('value', lambda o: o)\
                .is_string()\
                .is_between(1, 20, rule_sets={'foo1', 'foo2'})\
                .is_equals(20, rule_sets={'foo1'})

        response = validator.validate(21)
        self.assertEqual(len(response.errors), 3)

        response = validator.validate(22, 'foo1')
        self.assertEqual(len(response.errors), 2)

        response = validator.validate(21, 'foo2')
        self.assertEqual(len(response.errors), 1)

if __name__ == '__main__':
    unittest.main(exit=False)
