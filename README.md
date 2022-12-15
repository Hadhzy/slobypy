<h2 align="center"><b>slobypy</b>: ✨Python framework for React✨</h2>
<p align="center"><i>Based on sloby editor(web).</i></p>

<p align="center">
  <a href="https://github.com/FlurryGlo/Sloby">Sloby Editor</a> |
  </p>
</p>

-----------
<p align="center"><b>Use Python to design your own website from backend to frontend!</b></p>
<p align="center"><b>Alternatively, connect your existing Sloby frontend to your SlobyPy backend!</b></p>

## 📝 Table of Contents

- [📝 Table of Contents](#-table-of-contents)
- [ :information_source: About the project <a name = "about"></a>](#-about-)
- [🏁 Getting Started <a name = "getting_started"></a>](#-getting-started-)
    - [SCSS](#scss)
    - [HTML](#html)
    - [COMPONENT](#component)
- [⛏️ Built Using <a name = "built_using"></a>](#️-built-using-)
- [✍️ Authors <a name = "authors"></a>](#️-authors-)
- [💾 Docs  <a name = "docs"></a>](#-docs-)

--------------

## 📃 About <a name = "about"></a>

SlobyPy is a simple Python framework that can be used to develop awesome websites from frontend to backend. To achieve
this, SlobyPy allows you to use your existing HTML and CSS knowledge to develop similar frontend code, while maintaining
Pythonic syntax. Nonetheless, developing the backend is no harder! SlobyPy is able to stream data from Python to the
React frontend inside `Sloby` allowing for a seamless, performant, SSR-based experience via JIT compilation.

## 💾 Docs <a name = "docs"></a>

TBD

## 🏁 Getting started <a name = "getting_started"></a>

You can install SlobyPy via `pip` or your favorite PyPi package manager.

```bash
python -m pip install slobypy
```

Generate a new project with the following command:

```bash
python -m slobypy generate <project_name>
```

Start streaming JIT compiled data to Sloby:

```bash
python -m slobypy run
```

### SCSS

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
.base_class1{
 color:red;
 position:relative;
}
```

**Simple scss group**

```py
my_first_scss_group = SCSS_GROUP("first_scss_group")

my_class = SCSS_CLASS(
    name="my_class",
    color="red",
    position="relative",
)
my_class_2 = SCSS_CLASS(
    name="my_class_2",
    color="red",
    position="relative",
)

my_first_scss_group.add(my_class)
my_first_scss_group.relationship(my_class, child=my_class_2)
```

```
.my_class{
 color:red;
 position:relative;

.my_class_2{
 color:red;
 position:relative;
}}

```

--------------

### HTML

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
**With properties**

```py
p = P(P("child1"), color="red")
print(p.render())
```

```
<p color="red"><p >child1</p>
</p>
```

------------

### COMPONENT

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

[🎉**Contributors**🎉](https://github.com/FlurryGlo/slobypy/graphs/contributors)
