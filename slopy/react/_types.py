from typing import TypedDict
from slopy.react.component import Component
url_type = str
component_type = Component


class PATH_TYPE(TypedDict):
     url: url_type
     component: component_type

