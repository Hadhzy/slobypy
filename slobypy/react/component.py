#this project

# Third-Party
from abc import ABC, abstractmethod



class Component(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def render(self):
        """
        Define the elements here
        """
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
