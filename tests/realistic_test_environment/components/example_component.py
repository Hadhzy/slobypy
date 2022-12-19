from slobypy import *


@SlApp.component("/route1")
class MyComponent1(Component):

    @property
    def name(self):
        return "MyComponent1"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P("woo sloby is great", className="test1", onClick=self.on_click)
        yield MyComponent2(props={"important_data": "Woah1, this is a prop!"})


@SlApp.component("/route2")
class MyComponent2(Component):
    @property
    def name(self):
        return "MyComponent2"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P(self.props["important_data"], className="parent", onClick=self.on_click)
