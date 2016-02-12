class ValidationError(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs


class ValidationResponse(object):
    def __init__(self):
        self.is_valid = False
        self.errors = []


class ValueRule(object):
    def __init__(self, name, func, **kwargs):
        self.is_none_check = False
        self.rule_func = func
        self.validation_error = ValidationError(name, **kwargs)


class ValueRuleBook(object):
    def __init__(self, name, func):
        self.allow_none = True
        self.stop_on_first_error = False
        self.value_name = name
        self.value_func = func
        self.rules = []


class PyValidator(object):
    def __init__(self):
        self.all_stops_on_first_error = False
        self._current_name = None
        self._rulebooks = {}

    def validate(self, obj):
        if obj is None:
            raise ValueError('obj')

        response = ValidationResponse()

        print(len(self._rulebooks))
        for rulebook in self._rulebooks.values():
            value = rulebook.value_func(obj)
            for rule in rulebook.rules:
                if rulebook.allow_none and value is None and not rule.is_none_check:
                    print('i should not be here')
                    continue
                print('i should be here')
                if not rule.rule_func(value):
                    print('i should be here')
                    response.errors.append(rule.validation_error)

                if self.all_stops_on_first_error or rulebook.stop_on_first_error:
                    break

        response.is_valid = len(response.errors) > 0

        return response

    def stop_on_first_error(self):
        if self._current_name is None:
            self.all_stops_on_first_error = True
        else:
            self._rulebooks[self._current_name].stop_on_first_error = True

        return self

    def rule_for(self, name, func):
        self._assert_name_arg(name)
        self._assert_func_arg(func)
        self._current_name = name

        if name not in self._rulebooks:
            self._rulebooks[name] = ValueRuleBook(name, func)

        return self

    def not_none(self, **kwargs):
        kwargs = self._set_error_message('not none', **kwargs)
        self._rulebooks[self._current_name].allow_none = False
        rule = ValueRule(self._current_name, lambda x: x is not None, **kwargs)
        rule.is_none_check = True
        self._rulebooks[self._current_name]\
            .rules\
            .append(rule)

        return self

    def must(self, func, **kwargs):
        kwargs = self._set_error_message('validation failed', **kwargs)
        self._assert_func_arg(func)
        self._rulebooks[self._current_name]\
            .rules\
            .append(ValueRule(self._current_name, func, **kwargs))

        return self

    def must_be_string(self,  **kwargs):
        kwargs = self._set_error_message('must be string', **kwargs)
        return self.must(lambda x: isinstance(x, str), **kwargs)

    def must_be_int(self, **kwargs):
        kwargs = self._set_error_message('must be int', **kwargs)
        return self.must(lambda x: isinstance(x, int), **kwargs)

    def must_be_long(self, **kwargs):
        kwargs = self._set_error_message('must be long', **kwargs)
        return self.must(lambda x: isinstance(x, int), **kwargs)

    def must_be_float(self, **kwargs):
        kwargs = self._set_error_message('must be float', **kwargs)
        return self.must(lambda x: isinstance(x, float), **kwargs)

    def must_be_dict(self, **kwargs):
        kwargs = self._set_error_message('must be dict', **kwargs)
        return self.must(lambda x: isinstance(x, dict), **kwargs)

    def must_be_list(self, **kwargs):
        kwargs = self._set_error_message('must be list', **kwargs)
        return self.must(lambda x: isinstance(x, list), **kwargs)

    def must_be_greater_than(self, value, **kwargs):
        kwargs = self._set_error_message('must be greater', **kwargs)
        return self.must(lambda x: x > value, **kwargs)

    def must_be_less_than(self, value, **kwargs):
        kwargs = self._set_error_message('must be less than', **kwargs)
        return self.must(lambda x: x < value, **kwargs)

    def must_be_equal(self, value, **kwargs):
        kwargs = self._set_error_message('must be equal', **kwargs)
        return self.must(lambda x: x == value, **kwargs)

    @staticmethod
    def _set_error_message(default_message, **kwargs):
        if 'error_message' not in kwargs:
            kwargs['error_message'] = default_message

        return kwargs

    @staticmethod
    def _assert_name_arg(name):
        if name is None or not isinstance(name, str) or len(name) <= 1:
            raise ValueError('name')

    @staticmethod
    def _assert_func_arg(func):
        if func is None or not callable(func):
            raise ValueError('func')
