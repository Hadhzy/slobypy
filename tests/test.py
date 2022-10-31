from slopy.react.component import Component
from slopy.react.path import Path


@Path("test")
class MyFirstSlopyComponent(Component):
    def name(self):
        return "test"


@Path("second")
class MySecondSlopyComponent(Component):
    def name(self):
        return "test2"


print(Path.get_paths())
print(Path.get_paths()[0])

