# This Project
from slobypy.react import BaseElement

# Third-Party
from abc import ABC, abstractmethod
from typing import Generator, Type


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
        pass

    def render_js(self):
        """
        Non-mandatory method to render/include the js of the component
        """
        return ""

    def __str__(self) -> name:
        return self.__class__.__name__

    def __repr__(self):
        return f"Component({self.name})"
