class ValidationError(object):
    def __init__(self, name, **kwargs):
        self.name = name
        self.kwargs = kwargs

    def get(self, prepend=''):

        if prepend == '':
            name_formatted = self.name
        else:
            name_formatted = prepend + '.' + self.name

        return {
            'name': name_formatted,
            'kwargs': self.kwargs
        }
