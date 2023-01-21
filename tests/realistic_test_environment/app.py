from slobypy.react import *
from tests.realistic_test_environment.components.example_component import MyComponent1, MyComponent2, MyComponent3
from slobypy.react.component import *
from slobypy.react.context import Context


class Test:
    pass


class MyContext(Context):
    def create_data(self):
        yield {"test": 1}


class MyApp(AppComponent):
    def body(self):
        yield MyContext(MyComponent1())


MyApp()
