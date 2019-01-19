
class StoreException(Exception):
    def __init__(self, message):
        self.message = message

class StoreNotFoundError(StoreException):
    pass