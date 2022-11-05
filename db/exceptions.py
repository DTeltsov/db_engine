class InvalidValueError(Exception):
    def __init__(self, value, message='Invalid value:'):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.value}'


class NotFoundError(Exception):
    def __init__(self, item, message='not found'):
        self.item = item
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.item} {self.message}'


class AlredyExistsError(Exception):
    def __init__(self, item, message='alredy exists'):
        self.item = item
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.item} {self.message}'