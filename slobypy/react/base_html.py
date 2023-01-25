from __future__ import annotations

import string
from typing import Any, Callable, Iterable

from .. import react
from .component import Component
from .design import Design
from .scss import SCSS
from .scss_classes import SCSSClass
from .scss_properties import POSSIBLE_ATTRIBUTES

CLASS_NAME_PROPERTY = "className"
SCSS_GROUP_PROPERTY = "ScssGroup"


__all__: tuple[str, ...] = ("BaseElement",)


class BaseElement:
    tag: str = ""
    int_to_str = dict(zip([str(i) for i in range(10)], string.ascii_lowercase))
    scss_class = SCSSClass()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Slobypy BaseElement init is used to serve the element with features, and get the attributes.

        ### Arguments
        - *args: The content of the element.
        - **kwargs: The listeners the events and the inline css of the element.

        ### Returns
        - None
        """
        self.content: tuple[Any] = args
        new_kwargs = kwargs.copy()
        self.style = SCSS()  # scss instance
        self.class_names: list[Any] = []  # contain all the class_names
        self.listeners: dict[str, Callable[..., Any]] = {}  # contain all the listeners
        self._inline_scss(new_kwargs)  # handle inline css

        self._create_listeners(kwargs, new_kwargs)  # create listeners
        self.attrs: dict[str, Any] = new_kwargs  # set attributes
        self.parent: BaseElement | None = None  # parent element

        self._find_same_base_classes()  # check scss classes

    def _render_worker(self, tags: bool = False) -> str:
        rendered_html = f"<{self.tag}{self.render_attrs()}>" if tags else ""
        for element in self.content:
            if isinstance(element, (BaseElement, Component)):
                rendered_html += element.render() + "\n"
            else:
                rendered_html += str(element)

        rendered_html += f"</{self.tag}>" if tags else ""

        return rendered_html

    def _create_listeners(
        self, item: dict[str, Any], new_kwargs: dict[str, Any]
    ) -> None:
        for key, value in item.items():
            if callable(value):
                use_key = key
                key_split = key.split("on")
                if key_split[0] == "":
                    key_split[1] = key_split[1].capitalize()
                    use_key = "on".join(key_split)
                self.listeners[use_key] = value
                new_kwargs.pop(key)

    def _inline_scss(self, kwargs: dict[str, Any]) -> None:
        for key, value in kwargs.items():

            if key == CLASS_NAME_PROPERTY:
                self.class_names.append(
                    value
                )  # extend the class_names list with the actual classname

            # check if it is a valid property name
            if key in POSSIBLE_ATTRIBUTES:
                setattr(self.style, key, value)

    @staticmethod
    def get_element_classname(element: BaseElement) -> str | None:
        """
        This method is used to return the element "base(root)" classname.
        ### Arguments
        The element(itself)
        ### Returns
        value: the classname
        """

        for key, value in element.attrs.items():
            if key == CLASS_NAME_PROPERTY:
                return value
        return None

    def _find_same_base_classes(self) -> None:
        for (
            scss_global_class
        ) in react.Design.get_registered_classes():  # get all the classes
            scss_class: SCSSClass = scss_global_class["scss_class"]  # type: ignore
            if scss_class.properties["name"] == self.get_element_classname(
                self
            ):  # same classname match
                scss_class.check_scss_properties()  # check if the properties valid

                Design.USED_CLASSES.append(
                    scss_global_class
                )  # Add to the used class list

            if scss_class.properties["name"] != self.get_element_classname(self):
                scss_class.check_scss_properties()  # check if the properties valid

    def depth_of_the_element(self, element: BaseElement):
        """
         This method is used to return the depth of the element, depth -> integer, the element position from the component.

         ### Arguments
        - element: element

        ### Returns
        - int: the depth of the element.
        """

    def get_body_content(self) -> str:
        """
        This method is used to get the content of the element without tags by recursing through the element's children and
        rendering them to HTML.

        ### Arguments
        - None

        ### Returns
        - str: The html element as a string
        """

        return self._render_worker()

    def render(self) -> str:
        """
        This method is used to render the element with TAGS to HTML by recursing through the element's children and
        rendering them to HTML.

        ### Arguments
        - None

        ### Returns
        - str: The html element as a string
        """

        return self._render_worker(tags=True)

    def render_attrs(self) -> str:
        """
        This method is used to render the attributes of the element to HTML.

        ### Arguments
        - None

        ### Returns
        - str: The element's attributes as a string
        """
        return " ".join(
            [f' {key}="{value}"' for key, value in self.attrs.items()]
            + [
                f' {key}={{{"".join(self.int_to_str[n] for n in str(hash(value)))}}}'
                for key, value in self.listeners.items()
            ]
        )

    def render_js(self) -> str:
        """
        This method is used to render the js-side of the element, such as event listeners. This is done recursively
        in order to account for children

        ### Arguments
        - None

        ### Returns
        - str: The JavaScript code as a string
        """
        rendered_js: list[str] = []
        for element in self.content:
            if isinstance(element, (BaseElement, Component)):
                js = element.render_js()  # pylint: disable=invalid-name
                if js:
                    rendered_js.append(js)
        for _ in self.listeners.values():
            # TODO: Add js code to emit event over the socket
            # Using __hash__ to create a unique function name to prevent name collisions
            rendered_js.append(
                'function {processEvent}(e) {{\n  console.log("TBD")\n}}'
            )
        return "\n".join(rendered_js)

    # Todo: Extend this with kwargs
    def __iter__(self) -> Iterable[Any]:
        start = 0
        stop = len(self.content)
        curr = start
        while curr < stop:
            yield self.content[curr]
            curr += 1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.attrs})"

    def __str__(self) -> str:
        return self.render()
