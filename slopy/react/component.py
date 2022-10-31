from abc import ABC, abstractmethod

from ..rpc import Event


class Component(ABC):
    def on_click(self, event: Event):
        """
        This method is called when the component is clicked.

        ### Arguments
        - event: The `event` object that was emitted by `slopy`

        ### Returns
        - None
        """
        pass

    def on_hover_start(self, event: Event):
        """
        This method is called when the mouse enters the component.

        ### Arguments
        - event: The `event` object that was emitted by `slopy`

        ### Returns
        - None
        """
        pass

    def on_hover_end(self, event: Event):
        """
        This method is called when the mouse leaves the component.

        ### Arguments
        - event: The `event` object that was emitted by `slopy`

        ### Returns
        - None
        """
        pass

    def on_mount(self, event: Event):
        """
        This method is called when the component is mounted.

        ### Returns
        - None
        """
        pass
