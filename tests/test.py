from slobypy.app import SlApp
from slobypy.react import *
from slobypy.react.component import *


app = SlApp()


@app.component("firstcomponent/test")
class MyComponent1(Component):


    def name(self):
        return "test"

    def body(self):
        yield P("test")

    def mount(self):
        pass


@app.component("secondcomponent/test")
class MyComponent2(Component):
    def name(self):
        return "test"

    def body(self):
        yield P("test")

    def mount(self):
        print("here")


component1 = MyComponent1()
component2 = MyComponent2()
component2.mount()


#
