# This Project
from slobypy import SlApp


class NotSet:
    pass


NOT_SET = NotSet()


class Reactive:
    app: SlApp = None

    def __init__(self, value):
        self.value = value
        self.callbacks = []

    def __set__(self, obj, value):
        self.current_value = getattr(obj, self.public_name)
        if self.current_value != value:
            setattr(obj, self.internal_name, value)
            self.app.render(obj)

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.internal_name, NOT_SET)
        if not isinstance(value, NotSet):
            return value

    def __set_name__(self, owner, name):
        self.public_name = name
        self.internal_name = '_reactive_' + name
