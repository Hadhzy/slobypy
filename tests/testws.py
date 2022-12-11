from slobypy.app import SlApp as app
from slobypy.react import *
from slobypy.react.component import *

css = SCSSClass(
    name="parent",
    register=True
).child(
    SCSSClass(
        name="child1"
    ).child(SCSSClass(
        name="child1-child"
    ))
).child(SCSSClass(
    name="child2"
))


@app.component("/route1")
class MyComponent1(Component):
    @property
    def name(self):
        return "test"

    def on_click(self):
        print("click")

    def body(self):
        yield P("test", className="parent", onClick=self.on_click)
        yield MyComponent2(props={"test_prop_value": "the test value"})

    def mount(self):
        pass


class MyComponent2(Component):
    @property
    def name(self):
        return "test"

    def body(self):
        yield P(self.props["test_prop_value"])

    def mount(self):
        print("test prop:", self.props["test_prop_value"])


@app.component("secondcomponent/fake")
class FakeComponent(Component):
    @property
    def name(self):
        return "im a fake"

    def body(self):
        yield P("this is a fake prop, something is wrong, this shouldnt be rendered!")

    def mount(self):
        print("bad run")
