import inspect
from pyvalidator.call_stack import *
from pyvalidator.rules import *
from pyvalidator.response import *
from .value_config import *


class PyValidator(object):
    def __init__(self):
        self.all_stops_on_first_error = False
        self._current_name = None
        self._current_rule = None
        self._current_when_func = lambda o: True
        self._not_none = set()
        self._value_configs = {}
        self._rules = []

    def validate(self, obj_stack, rule_set='__all__', prepend=''):
        if obj_stack is None:
            raise ValueError('obj')
        if not isinstance(obj_stack, ObjCallStack):
            obj_stack = ObjCallStack(obj_stack)

        stopped_rules_for = set()

        if not isinstance(obj_stack, ObjCallStack):
            raise ValueError('obj_call_order')
        response = ValidationResponse()
        current_obj = obj_stack.top.obj

        for rule in self._rules:
            value_config = self._value_configs[rule.value_name]
            value = value_config.value_func(current_obj)

            if rule.value_name in stopped_rules_for or\
                    not self._execute_conditional_func(rule.when_func, current_obj, obj_stack) or\
                    not self._execute_conditional_func(rule.conditional_func, current_obj, obj_stack) or\
                    (
                        rule.value_name not in self._not_none and
                        value is None and
                        not isinstance(current_obj, NotNoneRule)
                    ) or\
                    (
                        rule_set != '__all__' and
                        rule_set not in rule.sets
                    ) or\
                    isinstance(rule, ValueRule) and self._execute_conditional_func(rule.rule_func, value, obj_stack):
                continue

            if isinstance(rule, ValueRule):
                response.errors.append(rule.validation_error.get(prepend))

                if self.all_stops_on_first_error or value_config.stop_on_first_error or rule.stop_on_error:
                    stopped_rules_for.add(rule.value_name)

            if isinstance(rule, ObjValidatorRule) and isinstance(value, list):
                response = self._merge_validation_response(self._validate_list_obj(value, obj_stack, rule.validator, rule_set, prepend + rule.value_name), response)
            elif isinstance(rule, ObjValidatorRule):
                    oc_copy = obj_stack.clone()
                    oc_copy.add(value)
                    response = self._merge_validation_response(rule.validator.validate(oc_copy, rule_set, prepend + rule.value_name), response)

        response.is_valid = len(response.errors) == 0

        return response

    def when(self, func):
        self._assert_func_arg(func)
        self._current_when_func = func

        return self

    def stop_on_first_error(self):
        if self._current_name is None:
            self.all_stops_on_first_error = True
        else:
            self._value_configs[self._current_name].stop_on_first_error = True

        return self

    def stop_on_error(self):
        if self._current_rule is None:
            raise AttributeError('Current rule not set')

        self._current_rule.stop_on_error = True

        return self

    def rules_for(self, name, func):
        self._assert_name_arg(name)
        self._assert_func_arg(func)
        self._current_name = name

        if name not in self._value_configs:
            self._value_configs[name] = ValueConfig(func)

        return self

    def not_none(self, **kwargs):
        kwargs = self._set_error_message('not none', **kwargs)
        self._not_none.add(self._current_name)
        rule = NotNoneRule(self._current_name, self._current_when_func,  **kwargs)
        rule.is_none_check = True
        self._current_rule = rule
        self._rules.append(rule)

        return self

    def must(self, value_func, **kwargs):
        if self._current_name is None:
            raise AttributeError('Current rule name not set')

        kwargs = self._set_error_message('validation failed', **kwargs)
        self._assert_func_arg(value_func)
        rule = ValueRule(self._current_name, value_func, self._current_when_func, **kwargs)
        self._current_rule = rule
        self._rules.append(rule)

        return self

    def is_string(self, **kwargs):
        kwargs = self._set_error_message('must be string', **kwargs)
        return self.must(lambda o: isinstance(o, str), **kwargs)

    def is_int(self, **kwargs):
        kwargs = self._set_error_message('must be int', **kwargs)
        return self.must(lambda o: isinstance(o, int), **kwargs)

    def is_long(self, **kwargs):
        kwargs = self._set_error_message('must be long', **kwargs)
        return self.must(lambda o: isinstance(o, int), **kwargs)

    def is_float(self, **kwargs):
        kwargs = self._set_error_message('must be float', **kwargs)
        return self.must(lambda o: isinstance(o, float), **kwargs)

    def is_dictionary(self, **kwargs):
        kwargs = self._set_error_message('must be dict', **kwargs)
        return self.must(lambda o: isinstance(o, dict), **kwargs)

    def is_list(self, **kwargs):
        kwargs = self._set_error_message('must be list', **kwargs)
        return self.must(lambda o: isinstance(o, list), **kwargs)

    def is_greater_than(self, value, **kwargs):
        kwargs = self._set_error_message('must be greater ' + str(value), **kwargs)
        return self.must(lambda o: o > value, **kwargs)

    def is_less_than(self, value, **kwargs):
        kwargs = self._set_error_message('must be less than', **kwargs)
        return self.must(lambda o: o < value, **kwargs)

    def is_between(self, head, tail, **kwargs):
        kwargs = self._set_error_message('must be between ' + str(head) + ' and ' + str(tail), **kwargs)
        return self.must(lambda o: o is not None and head <= o <= tail, **kwargs)

    def is_equals(self, value, **kwargs):
        kwargs = self._set_error_message('must be equal to ' + str(value), **kwargs)
        return self.must(lambda o: o == value, **kwargs)

    def is_length_equals(self, value, **kwargs):
        kwargs = self._set_error_message('must be length equals to ' + str(value), **kwargs)
        return self.must(lambda o: o is not None and len(o) == value, **kwargs)

    def is_length_between(self, head, tail, **kwargs):
        kwargs = self._set_error_message('must be length between ' + str(head) + ' and ' + str(tail), **kwargs)
        return self.must(
                lambda o: o is not None and head <= len(o) <= tail, **kwargs
            )

    def set_validator(self, validator, **kwargs):
        if not isinstance(validator, PyValidator):
            raise ValueError

        kwargs = self._set_error_message('Object validation', **kwargs)
        rule = ObjValidatorRule(self._current_name, validator, self._current_when_func, **kwargs)
        self._current_rule = rule
        self._rules.append(rule)

        return self

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

    @staticmethod
    def _execute_conditional_func(func, obj, obj_stack):
        if 'osc' in inspect.signature(func).parameters:
            return func(obj, obj_stack)
        return func(obj)

    @staticmethod
    def _validate_list_obj(objs, obj_stack, validator, rule_set, prepend):
        if not isinstance(objs, list):
            raise ValueError('objs')

        main_response = ValidationResponse()
        for idx, value in enumerate(objs):
            ocs_clone = obj_stack.clone()
            ocs_clone.add(value)
            value_response = validator.validate(ocs_clone, rule_set, prepend + '[' + str(idx) + ']')
            main_response = PyValidator._merge_validation_response(main_response, value_response)
        return main_response

    @staticmethod
    def _merge_validation_response(response1, response2):
        merged_response = ValidationResponse()
        if response1.is_valid is False or response2.is_valid is False:
                merged_response.is_valid = False
        merged_response.errors = response1.errors + response2.errors

        return merged_response
