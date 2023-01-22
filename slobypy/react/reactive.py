"""Used to create Reactive variables that automatically update the DOM"""

import slobypy  # DO NOT import the SlApp using from slobypy.app import SlApp as this will cause a circular import


class NotSet:  # pylint: disable=too-few-public-methods
    """Used to represent a variable that has not been set"""
    pass


NOT_SET = NotSet()

__all__: tuple[str, ...] = (
    "Reactive",
)

class Reactive:
    """
    By creating a Reactive variable, you can create a variable that will automatically update the DOM when it is changed.
    """

    def __init__(self, value) -> None:
        """
        Slobypy React init is used to re-render the component with the new data(like useEffect in react).

        ### Arguments
        - value: New value.

        ### Returns
        - None
        """
        self.current_value = None
        self.public_name = None
        self.internal_name = None

        self.value = value  # store the values
        self.callbacks = []  # store the callbacks

    def __set__(self, obj, value) -> None:
        self.current_value = getattr(obj, self.public_name)
        if self.current_value != value:
            setattr(obj, self.internal_name, value)
            slobypy.SlApp._render(obj)  # type: ignore

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.internal_name, NOT_SET)
        if not isinstance(value, NotSet):
            return value
        return None

    def __set_name__(self, owner, name) -> None:
        self.public_name = name
        self.internal_name = '_reactive_' + name
