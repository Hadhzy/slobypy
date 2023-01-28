from __future__ import annotations
# Built-in
from typing import Generator, Any

# This project
import slobypy.react.component as component_file
from slobypy.errors.react_errors import NotValidComponent

from .tools import *
__all__ = (
    "Context",
)


class Context:
    """
    Used to provide data transfer for the user.
    """
    def __init__(self, *components: "component_file.Component") -> None:
        """
        ### Arguments
         - components: Slobypy Components as an object -> Component().
        ### Returns
        - None
        """

        self.components = components  # Defined components by the user
        self.components_data: list = []  # Used to store the checked components

    # noinspection PyMethodMayBeStatic
    def create_data(self) -> Generator[Any, None, None]:  # type: ignore  # this comment should be deleted when the method will be implemented
        """Used to create the data by yielding it"""
        pass

    def run(self) -> None:
        """Used to render the components inside the context"""
        for component in self.components:

            self._check_component_type(component)  # check if it's a component

            self.components_data.append(component)  # add the component to the components_data after check

            for context_data in self.create_data():  # loop through the create_data in order to get the context_data

                if component_dict := find_component_in_app(component):  # Return the current dict(based on the component)
                    component_dict["context"] = context_data  # Add the context_data to the specific dict

    #noinspection PyMethodMayBeStatic
    def _check_component_type(self, component) -> None:
        if not isinstance(component, component_file.Component):
            raise NotValidComponent(f"{component} is not valid!")