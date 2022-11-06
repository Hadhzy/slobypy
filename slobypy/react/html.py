# Third-Party
from _html_types import SlobyPyCONTENT, SlobyPyATTRS


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


class A(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the a element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'a'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Abbr(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the abbr element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'abbr'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Address(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the address element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'address'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Area(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the area element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'area'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Article(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the article element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'article'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Aside(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the aside element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'aside'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Audio(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the audio element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'audio'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class B(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the b element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'b'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Base(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the base element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'base'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Bdi(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the bdi element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'bdi'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Bdo(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the bdo element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'bdo'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Blockquote(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the blockquote element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'blockquote'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Body(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the body element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'body'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Br(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the br element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'br'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


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
    tag = 'button'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Canvas(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the canvas element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'canvas'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Caption(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the caption element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'caption'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Cite(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the cite element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'cite'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Code(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the code element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'code'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Col(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the col element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'col'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Colgroup(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the colgroup element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'colgroup'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Data(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the data element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'data'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Datalist(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the datalist element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'datalist'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Dd(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the dd element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'dd'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Del(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the del element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'del'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Details(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the details element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'details'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Dfn(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the dfn element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'dfn'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Dialog(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the dialog element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'dialog'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Div(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the div element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'div'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Dl(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the dl element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'dl'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Dt(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the dt element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'dt'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Em(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the em element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'em'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Embed(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the embed element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'embed'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Fieldset(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the fieldset element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'fieldset'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Figcaption(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the figcaption element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'figcaption'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Figure(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the figure element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'figure'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Footer(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the footer element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'footer'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Form(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the form element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'form'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class H1(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the h1 element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'h1'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Head(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the head element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'head'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Header(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the header element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'header'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Hgroup(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the hgroup element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'hgroup'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Hr(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the hr element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'hr'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Html(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the html element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class I(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the i element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'i'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Iframe(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the iframe element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'iframe'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Img(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the img element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'img'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Input(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the input element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'input'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ins(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the ins element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'ins'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Kbd(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the kbd element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'kbd'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Label(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the label element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'label'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Legend(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the legend element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'legend'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Li(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the li element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'li'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Link(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the link element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'link'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Main(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the main element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'main'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Map(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the map element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'map'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Mark(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the mark element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'mark'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Menu(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the menu element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'menu'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Meta(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the meta element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'meta'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Meter(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the meter element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'meter'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Nav(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the nav element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'nav'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Noscript(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the noscript element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'noscript'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Object(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the object element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'object'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ol(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the ol element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'ol'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Optgroup(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the optgroup element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'optgroup'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Option(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the option element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'option'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Output(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the output element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'output'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class P(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the p element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'p'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Picture(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the picture element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'picture'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Portal(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the portal element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'portal'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Pre(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the pre element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'pre'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Progress(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the progress element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'progress'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Q(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the q element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'q'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Rp(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the rp element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'rp'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Rt(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the rt element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'rt'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ruby(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the ruby element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'ruby'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class S(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the s element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 's'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Samp(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the samp element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'samp'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Script(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the script element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'script'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Section(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the section element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'section'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Select(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the select element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'select'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Slot(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the slot element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'slot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Small(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the small element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'small'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Source(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the source element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'source'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Span(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the span element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'span'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Strong(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the strong element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'strong'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Style(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the style element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'style'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Sub(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the sub element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'sub'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Summary(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the summary element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'summary'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Sup(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the sup element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'sup'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Table(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the table element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tbody(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the tbody element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'tbody'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Td(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the td element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'td'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Template(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the template element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'template'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Textarea(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the textarea element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'textarea'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tfoot(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the tfoot element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'tfoot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Th(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the th element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'th'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Thead(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the thead element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'thead'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Time(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the time element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'time'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Title(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the title element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'title'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Tr(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the tr element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'tr'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Track(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the track element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'track'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class U(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the u element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'u'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Ul(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the ul element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'ul'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Var(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the var element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'var'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Video(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the video element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'video'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Wbr(BaseElement):
    """
    This class is used to create html elements for the `sloby` editor. This class will contain
    metadata and information about the wbr element.

    ### Arguments
    - *args: The content of the element
    - **kwargs: The attributes

    ### Returns
    - None
    """
    tag = 'wbr'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)