# this project
from slobypy.react._types import PATH_TYPE, url_type, component_type
from slobypy.react.tools import url_checker

# third-party
from typing import List


#FIXME: to get the PATHS list use properties.
class Path:
    """
   Path has 2 parts: the url and the component.

   ### Arguments
   - url: The url of the component

   ### Anomalies
   - When using this path decorator you don't have to pass out the component the decorator do it for you.
           """
    _PATHS = []

    @classmethod
    @property
    def PATHS(cls) -> List[PATH_TYPE]:
        return cls._PATHS

    def __init__(self, url: url_type) -> None:
        self.url = url if url_checker(url) else "Not valid url"  # error here

    def __eq__(self, other) -> bool:
        return self.url == other.url



    @classmethod
    def add_path(cls, path: PATH_TYPE) -> None:
        cls._PATHS.append(path)

    def __call__(self, component: component_type) -> None:
        self.add_path({"url": self.url, "component": component})