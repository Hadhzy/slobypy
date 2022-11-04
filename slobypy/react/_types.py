# This Project
from slobypy.react.component import Component

# Third-Party
from typing import TypedDict

url_type = str
component_type = Component


class PATH_TYPE(TypedDict):
    url: url_type
    component: component_type
