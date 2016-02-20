class ValueConfig(object):
    def __init__(self, value_func):
        self.value_func = value_func
        self.stop_on_first_error = False
        self.value_validator = None
