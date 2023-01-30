"""General utilities used throughout the React sub-package"""
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
from slobypy.errors.cli_errors import AlreadyExistsException
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
    """Used to handle the handler json file(add,delete, update)"""

    path: Path = ""

    @classmethod
    def analyse(cls) -> bool:
        """Start the handler json file creating process"""
        if cls.path:
            return True

        cls._create_file(cls.path)
        return False

    @classmethod
    def _create_file(cls, name):
        with open(name, "w") as file:
            file.write(SLO_DEBUG_HANDLER)

    @classmethod
    def set_path(cls, path: Path):
        """Used to set the path for the handler json file"""
        if not Path(path).exists():
            cls.path = path
        else:
            raise AlreadyExistsException(f"{path} is already exists")

    @classmethod
    def add_json(cls, base_key: str, sub_key: str, add_item: dict) -> None:
       """
       This method is used to add a new component to the handler json
       ### Arguments
        - base_key: registered_components | app_components
        - sub_key : component_route
        - add_item: component_data -> dict (uri, component, source_path, metadata, static)
       """
       json_data = cls._load()

       json_data[base_key][sub_key] = str(add_item)
       cls._dump(json_data)

    @classmethod
    def delete_json(cls, base_key: str, sub_key: str) -> None:
        """
         This method is used to delete a component from the handler json
         ### Arguments:
          -  base_key: registered_components | app_components
          -  sub_key : component_route
        """
        json_data = cls._load()

        del json_data[base_key][sub_key]

        cls._dump(json_data)

    @classmethod
    def _load(cls):
        with open(cls.path, "r") as f:
            data = json.load(f)
        return data

    @classmethod
    def _dump(cls, data):
        with open(cls.path, "w") as f:
            json.dump(data, f)
