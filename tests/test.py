from slobypy.react.scss_classes import SCSS_CLASS
from slobypy.react import *
import inspect

my_class = SCSS_CLASS(
    name="base_class",
    position="relative",
    child1=SCSS_CLASS(
        position="relative1"
    )
)

p = P("test", P("test", className="child1"), className="base_class")

