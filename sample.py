import re
from enum import Enum
from py_validator import *
import time
import memory_profiler


class ExternalMetaSource(Enum):
    business1 = 1
    business2 = 2


class ExternalMeta(object):
    def __init__(self):
        self.id = ''
        self.source = ''


class PhoneNumber(object):
    def __init__(self):
        self.code = ''
        self.number = ''


class User(object):
    def __init__(self):
        self.username = ''
        self.full_name = ''
        self.age = 0
        self.phone_numbers = []
        self.external = None


def valid_uuid(uuid):
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(uuid)
    return bool(match)


def main():
    phone_number1 = PhoneNumber()
    phone_number1.code = '916'
    phone_number1.number = '5556666'
    phone_number2 = PhoneNumber()
    phone_number2.code = None
    phone_number2.number = '5'
    phone_numbers = list()
    phone_numbers.append(phone_number1)
    phone_numbers.append(phone_number2)

    external = ExternalMeta()
    external.id = '8569d3b9-d9a0-4e0e-9511-defcd9974991'
    external.source = ExternalMetaSource.business1
    user = User()

    user.username = 'this'
    user.full_name = 'foo_name'
    user.password = 'secret'
    user.age = 25
    user.phone_numbers = phone_numbers
    user.external = external

    external_validator = PyValidator()\
        .rules_for('id', lambda o: o.id)\
            .must(lambda v: valid_uuid(v),  error_message='id is not a UUID', rule_sets={'update'})\
        .rules_for('source', lambda x: x.source)\
            .must(lambda v: v in ExternalMetaSource, error_message='source is not valid', rule_sets={'update'})

    phone_validator = PyValidator()\
        .rules_for('code', lambda o: o.code)\
            .not_none()\
            .is_string(error_message='must be 3 digit string', rule_sets={'update'})\
            .is_length_between(1, 3, error_message='code out of range', rule_sets={'update'})\
        .rules_for('number', lambda o: o.number)\
            .not_none()\
            .is_string(rule_sets={'update'})\
            .is_length_equals(7, error_message='must be length 7', rule_sets={'update'})\

    user_validator = PyValidator()\
        .rules_for('username', lambda x: x.username)\
            .stop_on_first_error()\
            .not_none()\
            .is_string()\
            .is_length_between(1, 20)\
        .rules_for('full_name', lambda x: x.full_name)\
            .stop_on_first_error()\
            .not_none(rule_sets={'update'})\
            .is_string(rule_sets={'update'})\
            .is_length_between(1, 2, rule_sets={'update'})\
        .rules_for('age', lambda x: x.age)\
            .stop_on_first_error()\
            .not_none(rule_sets={'update'})\
            .is_int(rule_sets={'update'})\
            .is_between(15, 21, rule_sets={'update'})\
        .rules_for('phone_numbers', lambda o: o.phone_numbers)\
            .set_validator(phone_validator, rule_sets={'update'})\
        .rules_for('external', lambda o: o.external)\
            .set_validator(external_validator, rule_sets={'update'})

    t1 = time.clock()
    # validate with all rules (no rule set defined)
    response = user_validator.validate(user)
    t2 = time.clock()

    print('Validation Passed: ' + str(response.is_valid))
    print('Number of errors: ' + str(len(response.errors)))
    print('Errors:')
    for error in response.errors:
        print(error)

    # Validation Passed: False
    # Number of errors: 6
    # Errors:
    # {'kwargs': {'error_message': 'not none'}, 'name': 'phone_numbers[1].code'}
    # {'kwargs': {'error_message': 'must be 3 digit string'}, 'name': 'phone_numbers[1].code'}
    # {'kwargs': {'error_message': 'code out of range'}, 'name': 'phone_numbers[1].code'}
    # {'kwargs': {'error_message': 'must be length 7'}, 'name': 'phone_numbers[1].number'}
    # {'kwargs': {'error_message': 'must be length between 1 and 2'}, 'name': 'full_name'}
    # {'kwargs': {'error_message': 'must be between 15 and 21'}, 'name': 'age'}

    print('Memory: {}Mb' .format(memory_profiler.memory_usage()))
    print('Executed in {} Seconds'.format(t2-t1))

    t1 = time.clock()
    # validate with update rules
    response = user_validator.validate(user, 'update')
    t2 = time.clock()

    print('Validation Passed: ' + str(response.is_valid))
    print('Number of errors: ' + str(len(response.errors)))
    print('Errors:')
    for error in response.errors:
        print(error)

    # Validation Passed: False
    # Number of errors: 5
    # Errors:
    # {'name': 'phone_numbers[1].code', 'kwargs': {'error_message': 'must be 3 digit string'}}
    # {'name': 'phone_numbers[1].code', 'kwargs': {'error_message': 'code out of range'}}
    # {'name': 'phone_numbers[1].number', 'kwargs': {'error_message': 'must be length 7'}}
    # {'name': 'full_name', 'kwargs': {'error_message': 'must be length between 1 and 2'}}
    # {'name': 'age', 'kwargs': {'error_message': 'must be between 15 and 21'}}

    print('Memory: {}Mb' .format(memory_profiler.memory_usage()))
    print('Executed in  {} Seconds'.format(t2-t1))

if __name__ == "__main__":
    main()
