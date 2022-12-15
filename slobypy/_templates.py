MAIN_FILE = """\
from slobypy.react import *

css = SCSSClass(
    name="parent",
    register=True
).child(
    SCSSClass(
        name="child1",
        display="block"
    ))
    
"""

COMPONENT_FILE = """\
from slobypy import SlApp
from slobypy.react import *


@SlApp.component("/route1")
class MyComponent1(Component):
    @property
    def name(self):
        return "MyComponent1"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P("test", className="parent", onClick=self.on_click)
        yield MyComponent2(props={"important_data": "Woah, this is a prop!"})

    def mount(self):
        pass


@SlApp.component("/route2")
class MyComponent2(Component):
    @property
    def name(self):
        return "MyComponent2"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P(self.props["important_data"], className="parent", onClick=self.on_click)

    def mount(self):
        pass

"""

CONFIG = """\
{
  "name": "My Project",
  "version": "1.0.0",
  "description": "My Project",
  "main": "app.py",
  "components": "components/",
  "scss": "scss/",
  "runtime_tasks": [],
  "processed_css": "",
  "processed_js": ""
}
"""