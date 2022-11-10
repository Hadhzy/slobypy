# This Project
from slobypy.react.component import Component

# Third-Party
from typing import TypedDict

uri_type = str
component_type = Component


class PATH_TYPE(TypedDict):
    uri: uri_type
    component: component_type
