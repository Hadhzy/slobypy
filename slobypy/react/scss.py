"""Used to build anything related to SCSS"""
from typing import Any

from .scss_properties import POSSIBLE_ATTRIBUTES

__all__: tuple[str, ...] = ("SCSS",)


class SCSS:
    """
    This class is used to manage SCSS styling for the React frontend. This class will prevent the creation of non-css
    attributes and will raise errors for incorrectly set attributes

    ### Arguments
    - kwargs: The default CSS attributes to set

    ### Returns
    - str: The html element as a string
    """

    POSSIBLE_ATTRIBUTES = POSSIBLE_ATTRIBUTES

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if key not in self.POSSIBLE_ATTRIBUTES:
                raise AttributeError(f"Attribute {key} is not a valid CSS attribute")
            setattr(self, key, value)

    def __getattr__(self, item: str) -> Any:
        if item in self.POSSIBLE_ATTRIBUTES:
            return self.__dict__.get(item)
        raise AttributeError(f"Attribute {item} is not a valid CSS attribute")

    def render(self) -> str:
        """
        This method is used to render the SCSS attributes to website-ready CSS.

        ### Arguments
        - None

        ### Returns
        - str: The CSS data as a string
        """
        return "; ".join(
            [
                f"{key.replace('_', '-')}: {value}"
                if isinstance(value, str)
                else f"{key.replace('_', '-')}: {' '.join(value)}"
                for key, value in self.__dict__.items()
            ]
        )
