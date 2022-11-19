#This project
from slobypy.react.scss_classes import SCSS_CLASS
# Built-in


class Design:
    _REGISTERED_CLASSES: list = []

    @classmethod
    def register(cls, scss_class: list[SCSS_CLASS] | SCSS_CLASS):
        if isinstance(scss_class, list):
            for scss_class_item in scss_class:
                cls._REGISTERED_CLASSES.append(scss_class_item)

        if isinstance(scss_class, SCSS_CLASS):
            cls._REGISTERED_CLASSES.append(scss_class)

    @classmethod
    def get_registered_classes(cls) -> list[SCSS_CLASS]:
        return cls._REGISTERED_CLASSES











