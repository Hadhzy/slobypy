from slobypy.react.scss import SCSS


class SCSS_CLASS:
    STYLE_CLASS = SCSS()
    _STYLES: list = []  # contain the style of the classes

    #Todo: not start with an empty dict and the child body -> [{}, {position: relative}]
    def __init__(self, **kwargs) -> None:
        """
        Create scss classes.

        """
        self._style_data: dict = {}
        self.properties = kwargs
        depth = 0
        for key, value in kwargs.items():
            try:
                self.STYLE_CLASS.__setattr__(key, value)
                self._style_data[key] = value

                depth += 1
            except:  # Todo: a child or a not valid scss property, handle them.
                self.style_data[key] = {key: depth}

        self._STYLES.append(self._style_data)

    @property
    def style_data(self) -> dict:
        return self._style_data

    @classmethod
    def get_style_data(cls) -> list:
        return cls._STYLES

    def __str__(self) -> str:
        return f'{self.style_data}'
