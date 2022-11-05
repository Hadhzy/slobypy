# Third-Party
from _html_types import SlobyPyTAG, SlobyPyCONTENT, SlobyPyATTRS


class BaseElement:
    tag: SlobyPyTAG = ''
    __slots__ = ["content", "attrs"]

    def __init__(self, *args, **kwargs):
        self.content: SlobyPyCONTENT = args
        self.attrs: SlobyPyATTRS = kwargs

    def render(self) -> str:
        rendered_html = f"<{self.tag} {self.render_attrs()}>"
        for element in self.content:
            if isinstance(element, BaseElement):
                rendered_html += element.render() + "\n"
            else:
                rendered_html += str(element) + "\n"
        return rendered_html + f"</{self.tag}>"

    #TODO: cleaner way to do that with type hint
    def render_attrs(self) -> list[SlobyPyATTRS]:
        return [dict(attr_key=value) for attr_key, value in self.attrs.items()]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.attrs})'


class Button(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the button element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes


    ### Returns
    - None
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__


class P(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the paragraph element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes


    ### Returns
    - None
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.__class__.__name__




