from __future__ import annotations
# This Project
from .react import Component, Reactive
from .rpc import Event
from .react.tools import uri_checker
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
        Reactive.app = self

    def component(self, uri: str) -> Callable:
        """
        This decorator is used to register a component to the app.

        ### Arguments
        - uri (str): The uri of the component

        ### Returns
        - Callable: The decorator's wrapped callable
        """

        def wrap(component):
            instance = component()  # get the instance of it
            instance.meta_data = {"uri": uri, "hash_instance": hash(instance)}  # add the meta_data
            self.add(uri, instance)  # add the uri
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
        cls._components.append({"uri": uri_checker(uri), "component": component})

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

    def run(self, route="/"):
        """
        This method is used to run the app.

        ### Arguments
        - None

        ### Returns
        - None
        """
        print(self._render(route=route))

    def _check_props(self):
        pass

    def _render(self, obj=None, route: str = False) -> str:
        """
        This method is used to render the app to HTML.

        ### Arguments
        - obj (Any): The specific object to render
        - route (str): The route to render

        ### Returns
        - str: The HTML string
        """
        if obj:
            # Don't mount as this *should* be only run on a re-render
            return obj.render()
        elif route:
            for component in self._components:
                if component["uri"] == route:
                    component["component"].mount()
                    return component["component"].render()
        else:
            result = ""
            for component in self._components:
                component["component"].mount()
                component["component"].render()
                result += component["component"].render()
            return result
