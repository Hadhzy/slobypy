from slobypy.react.scss_properties import POSSIBLE_ATTRIBUTES


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

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __setattr__(self, key, value):
        if key in self.POSSIBLE_ATTRIBUTES:
            super().__setattr__(key, value)
        else:
            raise AttributeError(f"Attribute {key} is not a valid CSS attribute")

    def __getattr__(self, item):
        if item in self.POSSIBLE_ATTRIBUTES:
            return self.__dict__.get(item, None)
        raise AttributeError(f"Attribute {item} is not a valid CSS attribute")

    def render(self) -> str:
        return "; ".join([f"{key.replace('_', '-')}: {value}" if isinstance(
            value, str) else f"{key.replace('_', '-')}: {' '.join(value)}" for key, value in self.__dict__.items()])
