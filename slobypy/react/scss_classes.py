from slobypy.react.scss import SCSS
from slobypy.errors.scss_errors import PROPERTY_KEY_ERROR


class SCSS_CLASS:

    STYLE_CLASS = SCSS()

    def __init__(self, **kwargs) -> None:
        """
        Create scss classes.

        """
        self.style_data = {}
        self.properties = kwargs

        for key, value in kwargs.items():
            try:
                self.STYLE_CLASS.__setattr__(key, value)
                self.style_data[key] = value
            except:
                raise PROPERTY_KEY_ERROR(f"Not valid property key: {key} ")

    def __str__(self) -> str:
        return f'{self.style_data}'