#This project
from slobypy.react.scss import SCSS
from slobypy import react
# Built-in
from typing import Generator, Type


class SCSS_CLASS:
    STYLE_CLASS = SCSS()
    _STYLES: list = []  # contain the style of the classes

    def __init__(self, register=False, **kwargs) -> None:
        """
        Create scss classes.
        """

        if register:  # register it automatically
            react.Design.register(self)

        self.properties = kwargs
        self._style_data: list = []


        for key, value in kwargs.items():
            self._style_data.append({key: value})  # update local style data
            self.add_style_global(key=key, value=value)  # update global style data

    def check_scss_properties(self) -> None:
        """
        This method is used to check the scss properties, manually.
        """

        for key, value in self.properties.items():
            self.STYLE_CLASS.__setattr__(key, value)

    def add_class_style(self, *dict: dict | list[dict], key: str = "", value: str = "") -> None:
        """
        This method is used to add the style to the local class.
        ### Arguments
        - key: the key of the dictionary
        - value: the value of the dictionary
        - *dict: a single dict or a list of dicts
        ### Returns
        None
        """
        if dict:
            self._style_data.append(dict)
            self.add_style_global(dict)
        else:
            self._style_data.append({key: value})
            self.add_style_global(key=value, value=value)


    @classmethod
    def add_style_global(cls, *dict: dict | list[dict] | tuple, key: str = "", value: str = "") -> None:
        """
        This method is used to add the style to the class attributes(class system) !not to the instance.
        ### Arguments
        - key: the key of the dictionary
        - value: the value of the dictionary
        - *dict: a single dict or a list of dicts
        ### Returns
        None
        """
        if dict:
            cls._STYLES.append(dict)
        else:
            cls._STYLES.append({key: value})

    @property
    def style_data(self) -> list:
        """
        This method is used to return the styles as a list.
        ### Arguments
        None
        ### Returns
        list: the scss class local styles
        """
        return self._style_data

    @classmethod
    def get_styles(cls) -> list:
        """
        This method is used to return the scss_class system styles as a list(all of them).
        ### Arguments
        None
        ### Returns
        list: the scss_class system styles(every single scss class style)
         """
        return cls._STYLES

    def __str__(self) -> str:
        return f'{self._style_data}'

    def __iter__(self) -> Generator[Type[dict], None, None]:
        start = 0
        stop = len(self.style_data)
        curr = start

        while curr < stop:
            yield self._STYLES[curr]
            curr += 1