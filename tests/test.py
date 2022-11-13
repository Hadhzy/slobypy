from slobypy.react.scss_classes import SCSS_CLASS
from slobypy.react import *



my_class = SCSS_CLASS(
    name="base_class",
    position="relative",
    child1=SCSS_CLASS(

    )
)

my_class_2 = SCSS_CLASS(
    name="base_class",
    position="relative",
    child1=SCSS_CLASS(

    )
)
p = P("test", P("test", className="child1"), className="base_class")


print(p.content)
print(SCSS_CLASS.STYLES)