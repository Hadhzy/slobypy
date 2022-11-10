class NotSet:
    pass


NOT_SET = NotSet()


class Reactive:
    app = None

    def __init__(self, value) -> None:
        """

        Slobypy React init is used to re-render the component with the new data(like useEffect in react).

        ### Arguments
        - value: New value.

        ### Returns
        - None
        """

        self.value = value  # store the values
        self.callbacks = []  # store the callbacks

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
