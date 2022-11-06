from ._html_types import SlobyPyCONTENT, SlobyPyATTRS


class BaseElement:
    tag: str = ''
    __slots__ = ["content", "attrs"]

    def __init__(self, *args, **kwargs):
        self.content: SlobyPyCONTENT = args
        self.attrs: SlobyPyATTRS = kwargs

    def render(self) -> str:
        """
        This method is used to render the element to HTML by recursing through the element's children and
        rendering them to HTML.

        ### Arguments
        - None

        ### Returns
        - str: The html element as a string
        """
        rendered_html = f"<{self.tag} {self.render_attrs()}>"
        for element in self.content:
            if isinstance(element, BaseElement):
                rendered_html += element.render() + "\n"
            else:
                rendered_html += str(element) + "\n"
        return rendered_html + f"</{self.tag}>"

    def render_attrs(self) -> str:
        """
        This method is used to render the attributes of the element to HTML.

        ### Arguments
        - None

        ### Returns
        - str: The element's attributes as a string
        """
        return " ".join([f'{key}="{value}"' for key, value in self.attrs.items()])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.attrs})'

    def __str__(self) -> str:
        return self.__class__.__name__
