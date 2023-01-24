from __future__ import annotations
# Built-in
from typing import Generator, Any

# This project
from slobypy.errors.react_errors import NotValidComponent
import slobypy.react.component as cmp

__all__ = (
    "Context",
)


class Context:
    DATA: list = []
    _components: list = []  # Used to define the components in the context.

    def __init__(self, *components: cmp.Component) -> None:
        self.components = components
        self.run()

    # noinspection PyMethodMayBeStatic
    def create_data(self) -> Generator[Any, None, None]:  # type: ignore  # this comment should be deleted when the method will be implemented
        """Used to create the data by yielding it"""
        pass

    def run(self) -> None:
        """Used to render the components inside the context"""
        for component in self.components:
            self._check_component_type(component)

            self._components.append(component)
            if context_data := self.get_data():
                component.context = context_data  # type: ignore

    def get_data(self) -> list:
        """Used to load the data from the create_data"""
        context_data = []
        for data in self.create_data():
            context_data.append(data)

        return context_data

    #noinspection PyMethodMayBeStatic
    def _check_component_type(self, component) -> None:
        if not isinstance(component, cmp.Component):
            raise NotValidComponent(f"{component} is not valid!")