#PyValidator

##The basics
    user = User()
    user.first_name = 'foo'
    user.last_name = 10
    user.age = 16
    user.email = 'foo@bar.com'

        validator = PyValidator()\
        .rules_for('first_name', lambda u: u.first_name)\
            .is_string()\
            .must(lambda x: len(x) is 10)\
        .rules_for('last_name', lambda u: u.last_name)\
            .is_string(error_message='last_name is string')\
        .rules_for('email', lambda u: u.email)\
            .is_string()\
        .rules_for('age', lambda u: u.age)\
            .is_int()\
            .is_greater_than(18)\

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
                    'error_message': 'last_name is string'
                }
            },
            {
                'name': 'age',
                'kwargs':
                {
                    'error_message': 'must be greater than 18'
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

##Rule sets
Rule sets will allow you to tag what rule set is executed. A good use for this
is differing creation and update rules. Default is all rules will be ran.

    validator = PyValidator()\
        .rules_for('first_name', lambda u: u.first_name)\
            .is_string(rule_sets=Set(['create', 'update']))

    # executes only rules tagged as 'update'
    validator.validate(obj, rule_set='update')

    validator = PyValidator()\
        .rules_for('first_name', lambda u: u.first_name)\
            .is_string()\
        .rules_for('deposit_amount', lambda u:deposit_amount)
            .is_int()\
            .is_greater_than(0)\
            .is_less_than(500, conditional: lamda u: u.age < 18)\
        .rules_for('age', lambda u: u.age)\


    # executes only rules tagged as 'update'
    validator.validate(obj, 'update')

##Conditional rules
Conditional rules allows rules to only trigger when true.
If you use the 'when(func)' method any rules afterwards will be grouped with the same condition.
Until a new new 'when(func)' is declared. You can also pass the conditional argument
when declaring a rule to add a conditional specific to that rule.

    phone_validator = PyValidator()\
        .when(lambda p, ocs: ocs.top.previous.obj.type == 'business_contact')\
        .rules_for('code', lambda o: o.code)\
            .not_none()\
            .is_string()\
            .is_length_between(0, 3, conditional=lambda x, osc:osc.top.previous.obj.country == 'US')\
            .is_length_between(0, 5, conditional=lambda x, osc:osc.top.previous.obj.country == 'UK')\
        .rules_for('number', lambda o: o.number)\
            .not_none()\
            .is_string()\
            .is_length_equals(6, conditional=lambda x, osc:osc.top.previous.obj.country == 'US')\
            .is_length_equals(9, conditional=lambda x, osc:osc.top.previous.obj.country == 'UK')\

##Nested object validator
Object validator will validate a class object property (or list of class objects) against
a provided PyValidation

    validator = PyValidator()\
        .rules_for('first_name', lambda u: u.first_name)\
            .is_string()\
        .rules_for('phone_number', lambda u: u.phone_number)\
            .set_validator(phone_validator)
        .rules_for('addresses', lambda u: u.addresses)\
            .set_validator(address_validator)

##Object call stack
To access the object call stack you must add 'ocs' as an argument for your funcs.

    child = child()
    child.last_name = 'Foo'
    parent = Parent()
    parent.last_name = 'Foo'
    parent.child = child

    child_validator = PyValidator()\
        .rules_for('last_name', lambda c: c.last_name)\
            .is_string()\
            .must(lambda c, ocs: ocs.top.previous.obj.last_name == last_name)

    parent_validator = PyValidator()\
        .rules_for('last_name', lambda u: u.last_name)\
            .is_string()\
        .rules_for('child', lambda u: u.child)
            .set_validator(child_validator)

##Control flow for stopping validation
    # calling stop_on_first_error() before declaring the first rule
    # will be a global stop validation on first error for each property

    validator = PyValidator()\
        .stop_on_first_error()\
        .rules_for('first_name', lambda u: u.first_name)\
            .is_string()\

    # calling stop_on_first_error() after a 'rules_for' will stop on first error
    # for that property and skip to the next property rules

    validator = PyValidator()\
        .rules_for('first_name', lambda u: u.first_name)\
            .stop_on_first_error()\
            .is_string()\

    # calling stop_on_error() will stop processing rules for that property on error
    # and continue to the next property rules

    validator = PyValidator()\
        .rules_for('first_name', lambda u: u.first_name)\
            .is_string()\
                .stop_on_error()\
            .must(lambda x: len(x) is 10)\
