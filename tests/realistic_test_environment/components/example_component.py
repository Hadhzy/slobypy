from slobypy.react import *
from slobypy import *


@SlApp.component("/route1")
class MyComponent1(Component):
    @property
    def name(self):
        return "MyComponent1"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P("test1", onClick=self.on_click)
        yield MyComponent2(props={"important_data": "Woah, this is a hahao10!"})


@SlApp.component("/route3")
class MyComponent3(Component):
    @property
    def name(self):
        return "MyComponent1"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P(self.context, onClick=self.on_click)



class MyComponent2(Component):
    @property
    def name(self):
        return "MyComponent2"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P(self.props["important_data"], onClick=self.on_click)