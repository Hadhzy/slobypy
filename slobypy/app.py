# This Project
from .react import Component
from .rpc import Event

# Third-Party
from typing import Union, Any, Callable, Type


class SlApp:
    """
    The main app class used to interact with and connect all the different components of SlobyPy as well as
    transmitting this data to the React frontend.

    ### Arguments
    - None

    ### Returns
    - None
    """
    # Use list to prevent name conflicts
    _components = []

    def __init__(self):
        pass

    def component(self, uri: str) -> Callable:
        """
        This decorator is used to register a component to the app.

        ### Arguments
        - uri (str): The uri of the component

        ### Returns
        - Callable: The decorator's wrapped callable
        """

        def wrap(component):
            self.add(uri, component())
            return component

        return wrap

    @classmethod
    def add(cls, uri: str, component: Type[Component]) -> None:
        """
        This method is used to add a component to the app.

        ### Arguments
        - uri (str): The uri of the component
        - component (Type[Component]): The component to add

        ### Returns
        - None
        """
        # TODO: Add URI checking regex
        cls._components.append({"uri": uri, "component": component})

    def dispatch(self, event: Union[Event, Any]) -> None:
        """
        This method is used to emit an event to the targeted component.

        ### Arguments
        - event (Union[Event, Any]): The event data to emit

        ### Returns
        - None
        """
        for component in self._components:
            if component.name() == event.name:
                try:
                    getattr(component, "on_" + event.type)(event)
                except AttributeError:
                    pass
