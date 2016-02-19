from pyvalidator.response import *


class BaseRule(object):
    def __init__(self, value_name, when_func, **kwargs):
        self.value_name = value_name
        self.value_validator = None
        self.stop_on_error = False
        result = self._kwargs_get_isinstance(set, 'rule_sets', {'__all__'}, **kwargs)
        self.sets = result[0]
        kwargs = result[1]
        result = self._kwargs_get_callable('conditional', lambda o: True, **kwargs)
        self.conditional_func = result[0]
        kwargs = result[1]
        self.when_func = when_func
        self.validation_error = ValidationError(value_name, **kwargs)

    @staticmethod
    def _kwargs_get_callable(key, default,  **kwargs):
        value = default
        if key in kwargs:
            if callable(kwargs[key]):
                value = kwargs[key]
                kwargs.pop(key)
            else:
                print(key)
                raise ValueError

        return value, kwargs

    @staticmethod
    def _kwargs_get_isinstance(instance_type, key, default,  **kwargs):
        value = default
        if key in kwargs:
            if isinstance(kwargs[key], instance_type):
                value = kwargs[key]
                kwargs.pop(key)
            else:
                raise ValueError

        return value, kwargs
