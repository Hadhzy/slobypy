# pylint: disable=unnecessary-pass

from __future__ import annotations

# Built-in
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generator, Type

# This project
from slobypy.react.scss import SCSS
from slobypy.errors.react_errors import NotValidComponent
from .tools import *
import slobypy.app as app

import slobypy.react.context as ctx

if TYPE_CHECKING:
    from slobypy.react import BaseElement  # type: ignore
    from typing import Self  # type: ignore # for python versions < 3.11


__all__: tuple[str, ...] = (
    "Component",
    "AppComponent",
)


class Component(ABC):
    """Base Component"""
    def __new__(cls, props=None, *args, **kwargs):
        # noinspection PyTypeChecker
        component = super().__new__(cls, *args, **kwargs)
        # noinspection PyProtectedMember
        for registered_component in app.SlApp._components:
            if registered_component["component"] == cls:
                component.meta_data = registered_component["metadata"]

        component.props = {} if props is None else props  # component props
        component.style = SCSS()  # Todo: Maybe remove?

        return component
    def __getattr__(self, item):

        if item == "context":  # return the specific context
            return find_component_in_app(self)["context"]

        return self.__getattr__(item)

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

    def render(self) -> str:
        """
        Get the component body with html elements and tags.
        """
        return ''.join([element.render() for element in self.body()])

    # noinspection PyMethodMayBeStatic
    def render_js(self) -> str:
        """
        Get any javascript code that is needed for the component
        """
        return ''.join([element.render_js() for element in self.body()])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Component('{self.name}')"


class AppComponent(ABC):
    """
    App based slobypy
    ------------------
    goal: Used to provide an app based view in the slobypy, where you can use wrappers(context), and more features.
    """
    _components: list = []  # Used to define the components in the app body

    def __init__(self) -> None:
        self.add_components()  # add components to the _components class variable

    @abstractmethod
    def body(self) -> Generator[Type[BaseElement] | Type[Component] | Type[ctx.Context], None, None]:
        """Used to define the components"""
        pass

    #noinspection PyProtectedMember
    #noinspection PyMethodMayBeStatic
    def _get_as_full_component(self, component):
        for register_component in app.SlApp._components:  # type: ignore
            if register_component["component"] == component:
                return register_component

    # noinspection PyProtectedMember
    def _find_component(self, element) -> None:
        for component in app.SlApp.only_components:  # type: ignore
            if isinstance(element, component):
                self._components.append(self._get_as_full_component(component))
                return
        else:
            raise NotValidComponent(f"{element} is not a valid component or context!")  # if the component in not valid or not registered

    # noinspection PyProtectedMember
    def add_components(self) -> None:
        """Used to add the components to the App"""
        for element in self.body():
            if isinstance(element, Component):
                self._find_component(element)  # make sure that this component is already registered by the user

            elif isinstance(element, ctx.Context):

                element.run()

                for component_element in element.components_data:
                    self._find_component(component_element)  # make sure that this component is already registered by the user




