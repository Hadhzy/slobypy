# This Project
from .rpc import Event
from .react.component import Component

# Third-Party
from typing import Type, Union, Any


class SlApp:
    def __init__(self):
        # Use list to prevent name conflicts
        self.components = []

    def component(self, component) -> Type[Component]:
        self.add(component)
        return component

    def add(self, component) -> None:
        self.components.append(component)

    def dispatch(self, event: Union[Event, Any]) -> None:
        for component in self.components:
            if component.name() == event.name:
                try:
                    getattr(component, "on_" + event.type)(event)
                except AttributeError:
                    pass
