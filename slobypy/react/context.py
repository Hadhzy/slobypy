from __future__ import annotations
# Built-in
from abc import ABC, abstractmethod

from typing import Generator, Any, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from slobypy.react.component import Component

__all__ = (
    "Context",
)


class Context:
    DATA: list = []
    _components: list = []  # Used to define the components in the context.
    def __init__(self, *components: Component) -> None:
        self.components = components

    # noinspection PyMethodMayBeStatic
    def create_data(self) -> Generator[Any, None, None]:
        """Used to create the data by yielding it"""
        pass
    def render(self) -> str:
        """Used to render the components inside the context"""
        returned_value = ""
        for component in self.components:

            self._components.append(component)

            component.context = self.get_data()
            if hasattr(component, "in_context"):
                component.in_context()

            returned_value += component.render()

        return returned_value

    def get_data(self) -> list:
        """Used to load the data from the create_data"""
        context_data = []
        for data in self.create_data():
            context_data.append(data)

        return context_data