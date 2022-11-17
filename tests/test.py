from slobypy.react.scss_classes import SCSS_CLASS
from slobypy.react import *
import inspect

# {"base_class": {"child1"}}
my_class = SCSS_CLASS(
    name="base_class",
    position="relative",
    child1=SCSS_CLASS(
        position="relative1"
    )
)

p = P("test", P("test"))

