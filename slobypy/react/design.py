# This project
from slobypy.react.scss_classes import SCSSClass


class Design:
    _REGISTERED_CLASSES: list = []
    USED_CLASSES: list = []  # Used scss class and scss group

    @classmethod
    def register(cls, scss_class: list[SCSSClass] | SCSSClass):
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

    @classmethod
    def get_registered_classes(cls) -> list[SCSSClass]:
        """Get the currently registered classes."""
        return cls._REGISTERED_CLASSES
