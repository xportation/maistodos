
class CashbackAddException(Exception):
    def __init__(self, message):
        self.message = message


class OrderAddException(Exception):
    def __init__(self, message):
        self.message = message
