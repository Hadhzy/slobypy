from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Iterable

from .. import react
from ..errors.scss_errors import NoName
from .scss import SCSS

if TYPE_CHECKING:
    from typing_extensions import Self

__all__: tuple[str, ...] = ("SCSSClass",)


class SCSSClass:
    STYLE_CLASS = SCSS()
    _STYLES: list[dict[str, str]] = []  # contain the style of the classes

    def __init__(self, register: bool = False, **kwargs: Any) -> None:
        """
        Create scss classes.
        """
        self.register: bool = False  # Register the parent

        if register:  # register it automatically
            react.Design.register(self, inspect.stack()[1].filename)
            self.register = True

        self.properties: dict[str, Any] = kwargs
        self._style_data: list[dict[str, Any]] = []
        self.child_classes: list[dict[Self, SCSSClass]] = []
        self.render_group: str = ""

        for key, value in kwargs.items():
            self._style_data.append({key: value})  # update local style data
            self.add_style_global(key=key, value=value)  # update global style data

    def child(self, child_scss_class: SCSSClass) -> Self:
        """
        Register a child
        ### Arguments
        child_scss_class: Self -> the child scss class
        ### Returns
        value: Self
        """
        if isinstance(child_scss_class, SCSSClass):  # type: ignore
            self.child_classes.append({self: child_scss_class})
        return self

    def render(self) -> str:
        """
        This method is used to render the whole scss class with children.
        """
        if not self.child_classes:  # without children
            return self.__render_single_class()
        return self._render()  # with children

    def _render(self, scss_class: SCSSClass | None = None) -> str:
        if scss_class is None:
            scss_class = self

        if self.register:
            scss_class.check_scss_properties()

        self.render_group += scss_class.__render_single_class()[  # pylint: disable=protected-access
            :-1
        ]  # render the parent

        for child_class in scss_class.child_classes:

            for value in child_class.values():

                if value.child_classes:
                    self.render_group += "\n"
                    self._render(value)  # there is child

                else:
                    self.render_group += value.__render_single_class()  # pylint: disable=protected-access
            self.render_group += "\n"

        self.render_group += "}"
        return self.render_group

    def __render_single_class(self) -> str:
        """
        This method is used to render the scss single class.
        """
        curr = ""
        end = "}"

        if "name" not in self.properties:  # THE NAME SHOULD BE THE FIRST PARAMETER
            raise NoName("You should define a name!")

        curr += "." + self.properties["name"] + "{"  # add the name into it

        for key, value in self.properties.items():

            if key == "name":  # skip the name property
                continue

            curr += f"\n {key}:{value};"  # make one line

        curr += "\n" + end
        return curr

    def check_scss_properties(self) -> None:
        """
        This method is used to check the scss properties, manually.
        """
        for key, value in self.properties.items():
            setattr(self.STYLE_CLASS, key, value)

    def add_class_style(
        self, *scss_class_dict: dict[str, str], key: str = "", value: str = ""
    ) -> None:
        """
        This method is used to add the style to the local class.
        ### Arguments
        - key: the key of the dictionary
        - value: the value of the dictionary
        - *dict: a single dict or a list of dicts
        ### Returns
        None
        """
        if scss_class_dict:
            self._style_data.extend(scss_class_dict)
            self.add_style_global(*scss_class_dict)
        else:
            self._style_data.append({key: value})
            self.add_style_global(key=value, value=value)

    @classmethod
    def add_style_global(
        cls, *mapping: dict[str, str], key: str = "", value: str = ""
    ) -> None:
        """
        This method is used to add the style to the class attributes(class system) !not to the instance.
        ### Arguments
        - key: the key of the dictionary
        - value: the value of the dictionary
        - *dict: a single dict or a list of dicts
        ### Returns
        None
        """
        if mapping:
            cls._STYLES.extend(mapping)
        else:
            cls._STYLES.append({key: value})

    @property
    def style_data(self) -> list[dict[str, Any]]:
        """
        This method is used to return the styles as a list.
        ### Arguments
        None
        ### Returns
        list: the scss class local styles
        """
        return self._style_data

    @classmethod
    def get_styles(cls) -> list[dict[str, str]]:
        """
        This method is used to return the scss_class system styles as a list(all of them).
        ### Arguments
        None
        ### Returns
        list: the scss_class system styles(every single scss class style)
        """
        return cls._STYLES

    def __str__(self) -> str:
        return f"{self._style_data}"

    # Todo: Extend the iter with children
    def __iter__(self) -> Iterable[dict[str, str]]:
        start = 0
        stop = len(self.style_data)
        curr = start

        while curr < stop:
            yield self._STYLES[curr]
            curr += 1
