#This project
from slobypy.react.scss_classes import SCSSClass
from slobypy.react.scss_group import SCSSGroup
# Built-in


class Design:
    _REGISTERED_CLASSES: list = []

    @classmethod
    def register(cls, scss_class: list[SCSSClass] | SCSSClass | SCSSGroup):
        if isinstance(scss_class, list):
            for scss_class_item in scss_class:
                cls._REGISTERED_CLASSES.append(scss_class_item)

        if isinstance(scss_class, SCSSClass):
            if scss_class not in cls._REGISTERED_CLASSES:
                cls._REGISTERED_CLASSES.append(scss_class)

        if isinstance(scss_class, SCSSGroup):
            if scss_class not in cls._REGISTERED_CLASSES:
                cls._REGISTERED_CLASSES.append(scss_class)  # register the group

    @classmethod
    def get_registered_classes(cls) -> list[SCSSClass]:
        return cls._REGISTERED_CLASSES

    @classmethod
    def get_registered_groups(cls) -> list[SCSSGroup]:
        groups = []

        for scss_class in cls.get_registered_classes():

            if isinstance(scss_class, SCSSGroup):
                groups.append(scss_class)

        return groups
