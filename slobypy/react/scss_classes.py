from slobypy.react.scss import SCSS

class SCSS_CLASS:

    STYLE_CLASS = SCSS()

    def __init__(self, **kwargs) -> None:
        """
        Create scss classes.

        """
        self.style_data = {}
        self.properties = kwargs

        for key, value in kwargs.items():
            self.STYLE_CLASS.__setattr__(key, value)
            self.style_data[key] = value

    def __str__(self) -> str:
        return f'{self.style_data}'