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
        yield P("odd8", className="bg-green-600 font-bold", onClick=self.on_click)
        yield MyComponent2(props={"important_data": "Woah, this is a prop!"})

    def mount(self):
        pass


@SlApp.component("/route2")
class MyComponent2(Component):
    @property
    def name(self):
        return "MyComponent2"

    def on_click(self):
        print(self.name, "has been clicked! yes")

    def body(self):
        yield P(self.props["important_data"], className="parent", onClick=self.on_click)

    def mount(self):
        pass

