from slobypy.react import *

my_test_scss_class = SCSSClass(
    register=True,
    name="test1",
    color="blue",
).child(SCSSClass(
    name="test2",
    color="red"
))
