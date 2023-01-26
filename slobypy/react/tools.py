"""General utilities used throughout the react sub-package"""
from __future__ import annotations
# Third-Party
from urllib.parse import urlparse
from typing import TYPE_CHECKING

# This Project
from slobypy.errors.react_errors import URIError
import slobypy.app as application

if TYPE_CHECKING:
    from slobypy.react.component import Component
__all__: tuple[str, ...] = (
    "uri_checker",
)


def uri_checker(uri: str = False) -> str | bool:
    """
     ### Arguments
    - uri: The uri of the component

    ### Returns
    uri: if the uri is valid
    error: if the uri is not valid
    """
    if uri is False:
        return ""
    slobypy_result = urlparse(uri)

    if slobypy_result.path and slobypy_result.scheme is not True:
        return uri

    raise URIError("Not valid uri")


# noinspection PyProtectedMember
def find_component_in_app(instance: Component) -> bool | dict:
    for component in application.SlApp._components:
        if isinstance(instance, component["component"]):
            return component
    return False