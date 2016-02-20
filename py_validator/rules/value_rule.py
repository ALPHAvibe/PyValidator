from py_validator.rules import BaseRule


class ValueRule(BaseRule):
    def __init__(self, name, rule_func, when_func, **kwargs):
        BaseRule.__init__(self, name, when_func, **kwargs)
        self.rule_func = rule_func
