from __future__ import annotations

import inspect
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from .errors.pages import Page404
from .react.router import SloRouter
from .rpc import RPC, Event
from slobypy.react.tools import *
if TYPE_CHECKING:
    from .react.component import Component

__all__: tuple[str, ...] = ("SlApp",)


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
    _components: list[dict[str, Any]] = []  # (uri, component, source, metadata, static)
    only_components: list[type[Component]] = []  # registered components(only)
    rpc: RPC | None = None

    @classmethod
    def component(
        cls, uri: str | SloRouter, static: bool = False
    ) -> Callable[[type[Component]], type[Component]]:
        """
        This decorator is used to register a component to the app.

        ### Arguments
        - uri (str): The uri of the component
        - static (bool): Used to define whether the component should be pre-rendered by SlobyPy(static).
        ### Returns
        - Callable: The decorator's wrapped callable
        """

        def wrap(component: type[Component]) -> type[Component]:
            cls.add(
                uri, component, inspect.stack()[1].filename, {"uri": uri}, static
            )  # add the uri
            return component

        return wrap

    @classmethod
    def add(  # pylint: disable=too-many-arguments
        cls,
        uri: str | SloRouter,
        component: type[Component],
        source: str,
        metadata: dict[str, Any],
        static: bool = False,
    ) -> None:
        """
        This method is used to add a component to the app.
        ### Arguments
        - uri (str): The uri of the component
        - component (Type[Component]): The component to add
        - source (str): The source of the component
        ### Returns
        - None
        """
        if isinstance(uri, SloRouter):
            uri = uri.route

        component_data = {
            "uri": uri_checker(uri),
            "component": component,
            "source_path": Path(source),
            "metadata": metadata,
            "static": static,
        }

        cls._components.append(

               component_data
        )

        SloDebugHandler.add_json(base_key="registered_components", sub_key=uri_checker(uri), add_item=component_data)  # add the registered_component to the handler

        cls.only_components.append(component)

    @classmethod
    def dispatch(cls, event: Event | Any) -> None:
        """
        This method is used to emit an event to the targeted component.

        ### Arguments
        - event (Union[Event, Any]): The event data to emit

        ### Returns
        - None
        """
        for component in cls._components:
            if component["component"].name() == event.name:
                try:
                    getattr(component, "on_" + event.type)(event)
                except AttributeError:
                    pass

    @classmethod
    def run(cls, *args: Any, **kwargs: Any) -> None:
        """
        This method is used to run the app.

        ### Arguments
        - None

        ### Returns
        - None
        """
        cls.rpc = RPC(cls, *args, **kwargs)

    # Todo:
    #   - Extend the render with more informal component data.
    @classmethod
    def _render(cls, obj: Component | None = None, route: str | None = None) -> str:
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
            return Page404(route=route).show()

        return "".join(
            component["component"]().render() for component in cls._components
        )
