"""Used to organize the overall design produce of th SCSS system"""
from .scss_classes import SCSSClass

__all__: tuple[str, ...] = ("Design",)


class Design:
    """
    Used to organize the overall design produce of th SCSS system
    """

    _REGISTERED_CLASSES: list[dict[str, str | SCSSClass]] = []
    USED_CLASSES: list[
        dict[str, str | SCSSClass]
    ] = []  # Used scss class and scss group

    @classmethod
    def register(
        cls, scss_class: list[SCSSClass] | SCSSClass, source_path: str
    ) -> None:
        """
        This method is used to register the scss class.

        ### Arguments
        - scss_class (list[SCSSClass] | SCSSClass | SCSSGroup): A list of scss classes to register

        ### Returns
        - None
        """

        if isinstance(scss_class, list):
            for scss_class_item in scss_class:
                cls._REGISTERED_CLASSES.append(
                    {"scss_class": scss_class_item, "source_path": source_path}
                )

        if isinstance(scss_class, SCSSClass):
            if scss_class not in cls._REGISTERED_CLASSES:  # type: ignore
                cls._REGISTERED_CLASSES.append(
                    {"scss_class": scss_class, "source_path": source_path}
                )

    @classmethod
    def get_registered_classes(cls) -> list[dict[str, str | SCSSClass]]:
        """Get the currently registered classes."""
        return cls._REGISTERED_CLASSES
