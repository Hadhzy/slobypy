from slopy.react.component import Component


class MyFirstSlopyComponent(Component):
    def name(self):
        return "something"

    def path(self):
        return "testurl"



myfirst = MyFirstSlopyComponent()
result = myfirst.path()
print(result)