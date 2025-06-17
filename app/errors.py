class Missing(Exception):
    # Handling the exception of missed data
    def __init__(self, msg: str):
        self.msg = msg


class Duplicate(Exception):
    # Handling the exception of duplicated data
    def __init__(self, msg: str):
        self.msg = msg
