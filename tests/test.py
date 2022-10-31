from slopy.react.component import Component
from slopy.react.path import Path


@Path("test")
class MyFirstSlopyComponent(Component):
    def name(self):
        return "name"
    def path(self):
        return "path"


print(Path.PATH)