"""General utilities used throughout the react sub-package"""
from __future__ import annotations
# Third-Party
from urllib.parse import urlparse
from typing import TYPE_CHECKING
from pathlib import Path
import json
# This Project
from slobypy.errors.react_errors import URIError
import slobypy.app as application
from slobypy._templates import SLO_DEBUG_HANDLER
if TYPE_CHECKING:
    from slobypy.react.component import Component

__all__: tuple[str, ...] = (
    "uri_checker",
    "find_component_in_app",
    "SloDebugHandler",
)


def uri_checker(uri: str = "") -> str | bool:
    """
     ### Arguments
    - uri: The uri of the component

    ### Returns
    uri: if the uri is valid
    error: if the uri is not valid
    """

    if not uri:
        return ""

    slobypy_result = urlparse(uri)

    if slobypy_result.path and slobypy_result.scheme is not True:
        return uri

    raise URIError("Not valid uri")


# noinspection PyProtectedMember
def find_component_in_app(instance: "Component") -> bool | dict:
    for component in application.SlApp._components:
        if isinstance(instance, component["component"]):
            return component
    return False


class SloDebugHandler:

    path: Path = Path()

    @classmethod
    def analyse(cls):

        if cls.path.exists():
            return True

        cls._create_file(cls.path)
        return False

    @classmethod
    def _create_file(cls, name):
        with open(name, "w") as file:
            file.write(SLO_DEBUG_HANDLER)

    @classmethod
    def set_path(cls, path: Path):
        cls.path = path

    @classmethod
    def add_json(cls, add_item: dict):
        with open(cls.path, "w") as file:
            file.write(json.dumps(add_item))

    @classmethod
    def delete_json(cls, delete_item: str):
        with open(cls.path, "w") as file:

            data = json.load(file)
            removed_data = data.pop(delete_item)
            file.write(removed_data)
