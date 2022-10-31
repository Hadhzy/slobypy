from abc import ABC, abstractmethod
from slopy.react.path import Path

#FIXME: type hinting for the abstractmethods


class Component(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def path(self) -> Path:
        pass

    def __str__(self):
        return f"{self.name()}-{self.path()}"

    def __repr__(self):
        return f"Component({self.name()=}{self.path()=})"

    #FIXME: I didn't find these events
    # def on_hover_start(self, event: Event):
    #     """
    #     This method is called when the mouse enters the component.
    #
    #     ### Arguments
    #     - event: The `event` object that was emitted by `slopy`
    #
    #     ### Returns
    #     - None
    #     """
    #     pass
    #
    # def on_hover_end(self, event: Event):
    #     """
    #     This method is called when the mouse leaves the component.
    #
    #     ### Arguments
    #     - event: The `event` object that was emitted by `slopy`
    #
    #     ### Returns
    #     - None
    #     """
    #     pass
    #
    # def on_mount(self, event: Event):
    #     """
    #     This method is called when the component is mounted.
    #
    #     ### Returns
    #     - None
    #     """
    #     pass
