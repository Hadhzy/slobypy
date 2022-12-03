# This project
from slobypy.react.scss_classes import SCSSClass
from slobypy.react.scss_group import SCSSGroup


class Design:
    _REGISTERED_CLASSES: list = []

    @classmethod
    def register(cls, scss_class: list[SCSSClass] | SCSSClass | SCSSGroup):
        """
        This method is used to register the scss class.

        ### Arguments
        - scss_class (list[SCSSClass] | SCSSClass | SCSSGroup): A list of scss classes to register

        ### Returns
        - None
        """
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
        """Get the currently registered classes."""
        return cls._REGISTERED_CLASSES

    @classmethod
    def get_registered_groups(cls) -> list[SCSSGroup]:
        """
        This method is used to all the currently registered groups in the design.

        ### Arguments
        - None

        ### Returns
        - list[SCSSGroup]: A list of all the registered groups.
        """
        groups = []

        for scss_class in cls.get_registered_classes():
            if isinstance(scss_class, SCSSGroup):
                groups.append(scss_class)

        return groups
