from __future__ import annotations

from typing import Any, Generic, Iterable, TypeGuard, TypeVar

from . import component as cmp
from ..errors.react_errors import NotValidComponent

__all__ = ("Context",)

T = TypeVar("T")


class Context(Generic[T]):
    _components: list[
        cmp.Component
    ] = []  # Used to define the components in the context.

    def __init__(self, *components: cmp.Component) -> None:
        self.components = components
        self.run()

    def create_data(self) -> Iterable[T]:
        """Used to create the data by yielding it"""
        raise NotImplementedError

    def run(self) -> None:
        """Used to render the components inside the context"""
        for component in self.components:
            self._check_component_type(component)

            self._components.append(component)
            if context_data := self.get_data():
                setattr(component, "context", context_data)

    def get_data(self) -> list[T]:
        """Used to load the data from the create_data"""
        context_data: list[T] = []
        for data in self.create_data():
            context_data.append(data)

        return context_data

    def _check_component_type(self, component: Any) -> TypeGuard[cmp.Component]:
        if not isinstance(component, cmp.Component):
            raise NotValidComponent(f"{component} is not valid!")
        return True
