from __future__ import annotations

# Built-in
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generator, Type
if TYPE_CHECKING:
    from slobypy.react import BaseElement


class Component(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def body(self) -> Generator[Type[BaseElement], None, None]:
        """
        Define the elements here
        """
        pass

    def render(self):
        return ''.join([element.render() for element in self.body()])

    def render_js(self):
        """
        Non-mandatory method to render/include the js of the component
        """
        return ""

    def __str__(self) -> name:
        return self.__class__.__name__

    def __repr__(self):
        return f"Component({self.name})"
