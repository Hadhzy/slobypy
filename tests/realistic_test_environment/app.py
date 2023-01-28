from tests.realistic_test_environment.components.example_component import MyComponent1, MyComponent3
from slobypy.react.component import *
from slobypy.react.context import Context

class MyApp(AppComponent):
    def body(self):
        myContext = Context("Hello World")
        yield myContext(MyComponent3())


MyApp()
