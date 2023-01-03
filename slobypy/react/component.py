# pylint: disable=unnecessary-pass

from __future__ import annotations

# Built-in
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generator, Type

# This project
from slobypy import SlApp
from slobypy.react.scss import SCSS
from slobypy.errors.react_errors import NotRegistered
import slobypy.react.context as ctx
import slobypy.react.context as context

if TYPE_CHECKING:
    from slobypy.react import BaseElement


__all__ = (
    "Component",
    "AppComponent")


class Component(ABC):

    def __new__(cls, props=None, *args, **kwargs):
        # noinspection PyTypeChecker
        component = super().__new__(cls, *args, **kwargs)
        # noinspection PyProtectedMember
        for registered_component in SlApp._components:
            if registered_component["component"] == cls:
                component.meta_data = registered_component["metadata"]

        component.props = {} if props is None else props
        component.style = SCSS()

        return component

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of the component.
        """
        pass

    @abstractmethod
    def body(self) -> Generator[Type[BaseElement], None, None]:
        """
        Use the elements here with yield syntax.
        """
        pass

    def render(self):
        """
        Get the component body with html elements and tags.
        """
        return ''.join([element.render() for element in self.body()])

    # noinspection PyMethodMayBeStatic
    def render_js(self):
        """
        Get any javascript code that is needed for the component
        """
        return ''.join([element.render_js() for element in self.body()])

    def __str__(self) -> name:
        return self.name

    def __repr__(self) -> str:
        return f"Component('{self.name}')"


class AppComponent(ABC):
    """Used to handle the registered components"""
    _components: list = [Component]  # Used to define the components in the app body

    @abstractmethod
    def body(self) -> Generator[Type[BaseElement] | Type[Component] | Type[context.Context], None, None]:
        """Used to define the components"""
        pass

    def render(self) -> str:
        """Used to render the components"""
        returned_value = ""
        for element in self.body():

            if isinstance(element, Component):
                self._components.append(element)

            elif isinstance(element, ctx.Context):
                self._components.append(element._components)

            returned_value += element.render()

        return returned_value

