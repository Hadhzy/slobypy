from slobypy.app import SlApp
from slobypy.react import *
from slobypy.react.component import *

MyFistScssGroup = SCSSGroup("test_scss_group")

Design.register(MyFistScssGroup)

first_class = SCSSClass(
    name="parent",
    position="relative",
    color="red",
)


second_class = SCSSClass(
    name="child"
)

MyFistScssGroup.add(first_class)
MyFistScssGroup.relationship(first_class, child=second_class)


app = SlApp()


@app.component("firstcomponent/test")
class MyComponent3(Component):
    def name(self):
        return "test"

    def body(self):
        yield P("parent text", P("child text", className="child"), ScssGroup="test_scss_group", className="parent")

    def mount(self):
        pass


@app.component("firstcomponent/test")
class MyComponent1(Component):

    def name(self):
        return "test"

    def body(self):
        yield P("test1", color="red")

    def mount(self):
        pass


@app.component("firstcomponent/test")
class MyComponent2(Component):
    def name(self):
        return "test"

    def body(self):
        yield MyComponent1(props={"test_prop_value": "the test value"})

    def mount(self):
        print("test prop:")


my_component2 = MyComponent2()
my_component1 = MyComponent1()



