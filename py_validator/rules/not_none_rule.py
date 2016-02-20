from py_validator.rules import ValueRule


class NotNoneRule(ValueRule):
    def __init__(self, name, when_func, **kwargs):
        ValueRule.__init__(self, name, lambda o: o is not None, when_func,  **kwargs)