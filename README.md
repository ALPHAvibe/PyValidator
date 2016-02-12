#PyValidator

##The basics

    user = User()
    user.first_name = 'foo'
    user.last_name = 10
    user.age = 16
    user.email = 'foo@bar.com'

    validator = PyValidator()\
    # declare 1rst rulebook for first name
    .rules_for('first_name', lambda u: u.first_name)\
        .must_be_string()\
        .must(lambda x: len(x) is 10)\
    # declare 2nd rulebook for last_name
    .rules_for('last_name', lambda k: k.last_name)\
        .must_be_string(error_message='lastname is string')\
    # declare 3rd rule_book for email
    .rules_for('email', lambda k: k.email)\
        .must_be_string()\
    # declare 4th rulebook for age
    .rules_for('age', lambda k: k.age)\
        .must_be_int()\
        .must_be_greater_than(18)\

    response = validator.validate(user)\

##The response
    {
        'is_valid': False
        'errors':
        [
            {
                'name': 'last_name',
                'kwargs':
                {
                    'error_message': 'lastname is string'
                }
            },
            {
                'name': 'age',
                'kwargs':
                {
                    'error_message': 'must be greater'
                }
            },
            {
                'name': 'first_name',
                'kwargs':
                {
                    'error_message': 'validation failed'
                }
            }
        ]
    }

##Control flow for stopping validation
    # calling stop_on_first_error() before declaring the first rule
    # will be a global stop validation on first error for each rulebook

    validator = PyValidator()\
    .stop_on_first_error()\
    .rules_for('first_name', lambda u: u.first_name)\
        .must_be_string()\

    # calling stop_on_first_error() after a rulebook will stop on first error
    # for that rulebook and skip to the next rulebook

    validator = PyValidator()\
    .rules_for('first_name', lambda u: u.first_name)\
        .stop_on_first_error()\
        .must_be_string()\

    # calling stop_on_error() will stop processing rules for that rulebook on error
    # and continue to the next rulebook

    validator = PyValidator()\
    .rules_for('first_name', lambda u: u.first_name)\
        .must_be_string()\
            .stop_on_error()\
        .must(lambda x: len(x) is 10)\

##Upcoming Features
##collection validator
collection validation will validate a list property againts a provided PyValidation

    validator = PyValidator()\
    .rules_for('first_name', lambda u: u.first_name)\
        .must_be_string()\
        .collection_validator('addresses',  lambda u: u.addresses, address_validator)

##rule sets
Rule sets will allow you to tag what set rules should be executed with.
You can pass rule set name to execute the membered rules only.

    validator = PyValidator()\
    .rules_for('first_name', lambda u: u.first_name)\
        .must_be_string(rulet_sets=Set(['create', 'update']))
        
    validator.validate(obj, rule_set='update')
