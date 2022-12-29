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
    def __init__(self, *components: Component) -> None:
        self.components = components
        self.add_data()
        self.pass_data_to_component()

    # noinspection PyMethodMayBeStatic
    def create_data(self) -> Generator[Any, None, None]:
        """Used to create the data by yielding it"""
        pass

    def add_data(self):
        for data in self.create_data():
            self.DATA.append(data)

    def pass_data_to_component(self):
        for component in self.components:
            component.context = self.DATA
            yield component

    def get_components(self) -> list[Component]:
        components = []
        for component in self.components:
            components.append(component)

        return components