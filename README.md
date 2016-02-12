#PyValidator

##the basics

    user = User()
    user.first_name = 'foo'
    user.last_name = 10
    user.age = 16
    user.email = 'foo@bar.com'

    validator = PyValidator()\
    .rule_for('first_name', lambda u: u.first_name)\
        .must_be_string()\
        .must(lambda x: len(x) is 10)\
    .rule_for('last_name', lambda k: k.last_name)\
        .must_be_string(error_message='lastname is string')\
    .rule_for('email', lambda k: k.email)\
        .must_be_string()\
    .rule_for('age', lambda k: k.age)\
        .must_be_int()\
        .must_be_greater_than(18)\

    response = validator.validate(user)\

# The response
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
