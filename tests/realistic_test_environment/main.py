from slobypy.react import *

css = SCSSClass(
    name="parent",
    register=True
).child(
    SCSSClass(
        name="child1",
        display="block"
    ))