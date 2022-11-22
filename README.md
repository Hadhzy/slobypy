<h2 align="center"><b>slobypy</b>: ✨Python framework for React✨</h2>
<p align="center"><i>Based on sloby editor(web).</i></p>

<p align="center">
  <a href="https://github.com/FlurryGlo/Sloby">Sloby Editor</a> |
  </p>
</p>

-----------

<p align="center"><b>You can build a website with the Sloby editor and you can connect with python(slobypy).</b></p>

**Simple scss class**
```py
my_class = SCSS_CLASS(
    name="base_class1",
    color="red",
    position="relative"
)

print(my_class.render())
```
```
.{
 name:base_class1;
 color:red;
 position:relative;
}
```
--------------------

**Simple html element**
```py
p = P("paragraph body", P("child1"))
print(p.render())
```
```
<p>paragraph body<p>child1</p>
</p>
```
-----------
**Simple component with abstract methods.**
```py
class MyFirstComponent(Component):
    def name(self):
        return "MyComponentName"

    def body(self):
        yield P("inside the component body")

    def mount(self):
        print("after registration")


component1 = MyFirstComponent()
print(component1.render())
```
```
<p >inside the component body</p>
```
-----------

**Component "registration" with the uri"**
```py
app = SlApp()

@app.component(uri="test/first")
class MyFirstComponent(Component):
  ...
```
