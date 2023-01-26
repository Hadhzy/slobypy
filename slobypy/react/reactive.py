"""Used to create Reactive variables that automatically update the DOM"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import slobypy

if TYPE_CHECKING:
    from typing_extensions import Self


class NotSet:  # pylint: disable=too-few-public-methods
    """Used to represent a variable that has not been set"""


NOT_SET = NotSet()

__all__: tuple[str, ...] = ("Reactive",)


class Reactive:
    """
    By creating a Reactive variable, you can create a variable that will automatically update the DOM when it is changed.
    """

    def __init__(self, value: Any) -> None:
        """
        Slobypy React init is used to re-render the component with the new data(like useEffect in react).

        ### Arguments
        - value: New value.

        ### Returns
        - None
        """
        self.current_value = None
        self.public_name: str = ""
        self.internal_name: str = ""

        self.value = value  # store the values
        self.callbacks = []  # store the callbacks

    def __set__(self, instance: Self | None, value: Any) -> None:
        self.current_value = getattr(instance, self.public_name)
        if self.current_value != value:
            setattr(instance, self.internal_name, value)
            slobypy.SlApp._render(instance)  # type: ignore

    def __get__(self, instance: Self | None, _=None):
        value = getattr(instance, self.internal_name, NOT_SET)
        if not isinstance(value, NotSet):
            return value
        return None

    def __set_name__(self, owner: Self, name: str) -> None:
        self.public_name = name
        self.internal_name = "_reactive_" + name
