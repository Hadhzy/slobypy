# This Project
from . import Component
from ._html_types import SlobyPyCONTENT, SlobyPyATTRS
from .scss import SCSS
from .scss_classes import SCSS_CLASS
from slobypy.errors.scss_errors import PROPERTY_KEY_ERROR
# Built-in
import string
from typing import Self


CLASS_NAME_PROPERTY = "className"


class BaseElement:
    tag: str = ''
    listeners: dict = {}
    scss_class = SCSS_CLASS()

    def __init__(self, *args, **kwargs) -> None:
        """
        Slobypy BaseElement init is used to serve the element with features, and get the attributes.

        ### Arguments
        - *args: The content of the element.
        - **kwargs: The listeners the events and the inline css of the element.

        ### Returns
        - None
        """

        self.content: SlobyPyCONTENT = args
        new_kwargs = kwargs.copy()

        self.style = SCSS()  # scss instance
        self.classNames: list = []  # contain all the classNames
        self._inline_scss(new_kwargs)  # handle inline css
        self._check_classname_in_scss(new_kwargs)  # check the valid classnames

        self._create_listeners(kwargs, new_kwargs)  # create listeners
        self.attrs: SlobyPyATTRS = new_kwargs  # set attributes

        self.parent: Self = None  # parent element



    def _render_worker(self, tags=None) -> str:
        rendered_html = f"<{self.tag} {self.render_attrs()}>" if tags else ""
        for element in self.content:
            if isinstance(element, BaseElement) or isinstance(element, Component):

                rendered_html += element.render() + "\n"
            else:
                rendered_html += str(element)

        rendered_html += f"</{self.tag}>" if tags else ""

        return rendered_html

    def _create_listeners(self, item, new_kwargs):
        for key, value in item.items():
            if callable(value):
                use_key = key
                key_split = key.split("on")
                if key_split[0] == '':
                    key_split[1] = key_split[1].capitalize()
                    use_key = "on".join(key_split)
                self.listeners[use_key] = value
                new_kwargs.pop(key)

    def _inline_scss(self, kwargs):
        for key, value in kwargs.items():
            if key == CLASS_NAME_PROPERTY:
                self.classNames.append(value)  # extend the classNames list with the actual classname

            self.style.__setattr__(key, value)  # check if it is a valid property name



    # Todo: finish the classname check
    def _check_classname_in_scss(self, kwargs):
        current_style_dict = None  # current scss class
        content_element_end = False

        for key, value in kwargs.items():
            if key == CLASS_NAME_PROPERTY:
                for style_dict in self.scss_class.get_style_data():
                    try:
                        if style_dict["name"] == value:
                            current_style_dict = style_dict
                    except:
                        continue
        for content_element in self.content:
            if isinstance(content_element, type) and issubclass(content_element, BaseElement):  # class and subclass of the element
                for key, value in current_style_dict.items():
                    if key in self.classNames:
                        break
                else:
                    print("not valid scss handle")

                break


    def depth_of_the_element(self, element) -> int:
        """
        This method is used to return the depth of the element, depth -> integer, the element position from the component.

        ### Arguments
       - element: element

       ### Returns
       - int: the depth of the element.
        """
        pass

    def get_body_content(self):
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
        return " ".join([f'{key}="{value}"' for key, value in self.attrs.items()] +
                        [f'{key}={value.__name__}' for key, value in self.listeners.items()])

    def render_js(self) -> str:
        """
        This method is used to render the js-side of the element, such as event listeners. This is done recursively
        in order to account for children

        ### Arguments
        - None

        ### Returns
        - str: The JavaScript code as a string
        """
        letters = string.ascii_lowercase
        numbers = [str(i) for i in range(10)]
        int_to_str = dict(zip(numbers, letters))
        rendered_js = []
        for element in self.content:
            if isinstance(element, BaseElement) or isinstance(element, Component):
                js = element.render_js()
                if js:
                    rendered_js.append(js)
        for key, value in self.listeners.items():
            # TODO: Add js code to emit event over the socket
            # Using __hash__ to create a unique function name to prevent name collisions
            rendered_js.append(
                f'function {"".join(int_to_str[n] for n in str(value.__hash__()))}(e) {{\n  console.log("TBD")\n}}')
        return "\n".join(rendered_js)

    #Todo: create an iterator, that can loop through the elements.
    def __iter__(self):
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.attrs})'

    def __str__(self) -> str:
        return self.__class__.__name__
