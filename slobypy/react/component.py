# Third-Party
from abc import ABC, abstractmethod


class Component(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Component({self.name})"
