from py_validator.rules import BaseRule


class ObjValidatorRule(BaseRule):
    def __init__(self, name, validator, when_func, **kwargs):
        BaseRule.__init__(self, name, when_func, **kwargs)
        self.validator = validator
