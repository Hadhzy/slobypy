from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Generic, Iterable, TypeVar

from .. import app
from ..errors import NotValidComponent
from . import context as ctx
from .scss import SCSS

if TYPE_CHECKING:
    from typing_extensions import Self

    from slobypy.react import BaseElement


__all__: tuple[str, ...] = (
    "Component",
    "AppComponent",
)

T = TypeVar("T")


class Component(ABC):
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        # noinspection PyTypeChecker
        component = super().__new__(cls, *args, **kwargs)
        # noinspection PyProtectedMember
        for registered_component in app.SlApp._components:  # type: ignore  # pylint: disable=protected-access
            if registered_component["component"] == cls:
                setattr(component, "meta_data", registered_component["metadata"])

        setattr(component, "props", {} if args[0] is not None else args[0])
        setattr(component, "style", SCSS())
        return component

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Name of the component.
        """
        raise NotImplementedError

    @abstractmethod
    def body(self) -> Iterable[BaseElement]:
        """
        Use the elements here with yield syntax.
        """
        raise NotImplementedError

    def render(self) -> str:
        """
        Get the component body with html elements and tags.
        """
        return ''.join([element.render() for element in self.body()])

    def render_js(self) -> str:
        """
        Get any javascript code that is needed for the component
        """
        return ''.join([element.render_js() for element in self.body()])

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Component('{self.name}')"


class AppComponent(ABC, Generic[T]):
    """
    App based slobypy
    ------------------
    goal: Used to provide an app based view in the slobypy, where you can use wrappers(context), and more features.
    """
    _components: list[dict[str, Any]] = []  # Used to define the components in the app body

    def __init__(self) -> None:
        self.add_components()

    @abstractmethod
    def body(self) -> Iterable[type[BaseElement | Component | ctx.Context[T]]]:
        """Used to define the components"""
        raise NotImplementedError

    def _get_as_full_component(self, component: type[Component]) -> dict[str, Any] | None:
        for register_component in app.SlApp._components:  # type: ignore  # pylint: disable=protected-access
            if register_component["component"] == component:
                return register_component
        return None

    def _find_component(self, element: dict[str, Any]) -> None:
        for component in app.SlApp.only_components:
            if isinstance(element, component):
                cmp = self._get_as_full_component(component)
                if cmp:
                    self._components.append(cmp)
                return
        raise NotValidComponent(f"{element} is not a valid component or context!")

    def add_components(self) -> None:
        """Used to add the components to the App"""
        for element in self.body():
            if isinstance(element, Component):
                self._find_component(element)

            elif isinstance(element, ctx.Context):
                for component_element in element._components:  # type: ignore  # pylint: disable=protected-access
                    self._find_component(component_element)  # type: ignore
