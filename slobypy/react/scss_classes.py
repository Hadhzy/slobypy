#This project
from slobypy.react.scss import SCSS


class SCSS_CLASS:
    STYLE_CLASS = SCSS()
    _STYLES: list = []  # contain the style of the classes

    #Todo: not start with an empty dict and the child body -> [{}, {position: relative}]
    def __init__(self, **kwargs) -> None:
        """
        Create scss classes.

        """
        self.properties = kwargs
        self._style_data: list = []

        for key, value in kwargs.items():
            self.STYLE_CLASS.__setattr__(key, value)
            self._style_data.append({key: value})  # update local style data
            self.add_style(key, value)  # update global style data

    @classmethod
    def add_style(cls, key: str, value: str):
        cls._STYLES.append({key: value})

    @property
    def style_data(self) -> list:
        return self._style_data

    @classmethod
    def get_styles(cls) -> list:
        return cls._STYLES

    def __str__(self) -> str:
        return f'{self._style_data}'
