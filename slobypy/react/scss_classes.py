from slobypy.react.scss import SCSS


class SCSS_CLASS:
    STYLE_CLASS = SCSS()
    STYLES: list = []  # contain the style of the classes

    def __init__(self, **kwargs) -> None:
        """
        Create scss classes.

        """
        self.style_data: dict = {}
        self.properties = kwargs

        for key, value in kwargs.items():
            try:
                self.STYLE_CLASS.__setattr__(key, value)
                self.style_data[key] = value

                self.STYLES.append(self.style_data)  # add to the class attributes
                self.style_data = {}
            except:
                print("there is a child")


    @classmethod
    def get_style_data(cls) -> list:
        return cls.STYLES

    def __str__(self) -> str:
        return f'{self.style_data}'
