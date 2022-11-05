# Third-Party
from typing import Any, Tuple, Dict


class BaseElement:
    tag: str = ''

    def __init__(self, *args, **kwargs):
        self.content: Tuple[Any] = args
        self.attrs: Dict[str, Any] = kwargs

    def render(self) -> str:
        rendered_html = f"<{self.tag} {self.render_attrs()}>"
        for element in self.content:
            if isinstance(element, BaseElement):
                rendered_html += element.render() + "\n"
            else:
                rendered_html += str(element) + "\n"
        return rendered_html + f"</{self.tag}>"

    def render_attrs(self) -> str:
        return " ".join([f'{key}="{value}"' for key, value in self.attrs.items()])

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.attrs})'


class Button(BaseElement):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


button1 = Button()
print(button1.__repr__())
