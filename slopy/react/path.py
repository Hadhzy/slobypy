# this project
from slopy.react._types import PATH_TYPE, url_type, component_type
from slopy.react.tools import path_checker

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
    PATHS = []

    def __init__(self, url: url_type) -> None:
        self.url = url

    def __eq__(self, other) -> bool:
        return self.url == other.url

    @classmethod
    def get_paths(cls) -> List[PATH_TYPE]:
        return cls.PATHS

    @classmethod
    def add_path(cls, path: PATH_TYPE) -> None:
        cls.PATHS.append(path)

    def __call__(self, component: component_type) -> None:
        self.add_path({"url": self.url, "component": component})