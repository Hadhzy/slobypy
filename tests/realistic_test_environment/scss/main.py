from slobypy.react import *

my_test_scss_class = SCSSClass(
    register=True,
    name="test2",
    color="green",
).child(SCSSClass(
    name="test1",
    color="yellow"
))
