class PROPERTY_KEY_ERROR(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)