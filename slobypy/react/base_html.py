# This Project
from . import Component
from ._html_types import SlobyPyCONTENT, SlobyPyATTRS

# Built-in
import string


class BaseElement:
    tag: str = ''
    listeners: dict = {}
    __slots__ = ["content", "attrs"]

    def __init__(self, *args, **kwargs):
        self.content: SlobyPyCONTENT = args
        new_kwargs = kwargs.copy()
        for key, value in kwargs.items():
            if callable(value):
                use_key = key
                key_split = key.split("on")
                if key_split[0] == '':
                    key_split[1] = key_split[1].capitalize()
                    use_key = "on".join(key_split)
                self.listeners[use_key] = value
                new_kwargs.pop(key)
        self.attrs: SlobyPyATTRS = new_kwargs

    def _render_worker(self, tags=None) -> str:
        rendered_html = f"<{self.tag}{self.render_attrs()}>" if tags else ""
        for element in self.content:
            if isinstance(element, BaseElement) or isinstance(element, Component):
                rendered_html += element.render() + "\n"
            else:
                rendered_html += str(element)
        rendered_html += f"</{self.tag}>" if tags else ""
        return rendered_html

    def get_body_content(self):
        """
       This method is used to get the content of the element without tags by recursing through the element's children and
       rendering them to HTML.

       ### ArgumentsX
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

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.attrs})'

    def __str__(self) -> str:
        return self.__class__.__name__
