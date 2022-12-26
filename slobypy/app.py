from __future__ import annotations

# Third-Party
import inspect

# Built-in
from typing import TYPE_CHECKING, Union, Any, Callable, Type
from pathlib import Path

# This Project
from .rpc import Event, RPC
from .react.tools import uri_checker

if TYPE_CHECKING:
    from .react.component import Component


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
    rpc = None

    @classmethod
    def component(cls, uri: str, static: bool = False) -> Callable:
        """
        This decorator is used to register a component to the app.

        ### Arguments
        - uri (str): The uri of the component
        - static (bool): Used to define whether the component should be pre-rendered by SlobyPy(static).
        ### Returns
        - Callable: The decorator's wrapped callable
        """

        def wrap(component):
            cls.add(uri, component, inspect.stack()[1].filename, {"uri": uri})  # add the uri
            return component

        return wrap

    @classmethod
    def add(cls, uri: str, component: Type[Component], source, metadata, static: bool = False) -> None:
        """
        This method is used to add a component to the app.
        ### Arguments
        - uri (str): The uri of the component
        - component (Type[Component]): The component to add
        - source (str): The source of the component
        ### Returns
        - None
        """
        # TODO: Add URI checking regex
        cls._components.append(
            {"uri": uri_checker(uri), "component": component, "source_path": Path(source), "metadata": metadata, "static": static})

    @classmethod
    def dispatch(cls, event: Union[Event, Any]) -> None:
        """
        This method is used to emit an event to the targeted component.

        ### Arguments
        - event (Union[Event, Any]): The event data to emit

        ### Returns
        - None
        """
        for component in cls._components:
            if component.name() == event.name:
                try:
                    getattr(component, "on_" + event.type)(event)
                except AttributeError:
                    pass

    @classmethod
    def run(cls, *args, **kwargs):
        """
        This method is used to run the app.

        ### Arguments
        - None

        ### Returns
        - None
        """
        cls.rpc = RPC(cls, *args, **kwargs)

    def _check_props(self):
        pass

    # Todo: Extend the render with more informal component data.
    @classmethod
    def _render(cls, obj=None, route: str = False) -> tuple[Any, Any] | str | Any:
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

        if route:
            for component in cls._components:
                if component["uri"] == route:
                    return component["component"]().render()

        return "".join(component["component"]().render() for component in cls._components)
