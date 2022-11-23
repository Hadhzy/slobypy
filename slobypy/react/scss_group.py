from __future__ import annotations
# This project

# Built-in

from typing import TYPE_CHECKING, Self
from slobypy.errors.scss_errors import RELATIONSHIP_ERROR
import slobypy.react.scss_classes as scss



class SCSS_GROUP_BASE:
    def __init__(self, child_classes):
        self._child_classes = child_classes


    @property
    def child_classes(self) -> list[dict[scss.SCSS_CLASS, dict]]:
        return self._child_classes


class SCSS_GROUP(SCSS_GROUP_BASE):
    """
    This class is representing a group of scss classes
    """
    GROUPS: list = [Self]  # all-groups

    def __init__(self, name):
        self.GROUPS.append(self)  # update the global group
        self.name = name  # get the name
        self._child_classes: list[dict[scss.SCSS_CLASS]] = []  # store the local classes

        super().__init__(self._child_classes)  # pass the child_classes out


    def add(self, scss_class: scss.SCSS_CLASS):
        self._child_classes.append({scss_class: {"parent": "", "child": ""}})  # add a brand new scss_class to the local group

    def relationship(self, scss_class: scss.SCSS_CLASS, parent: scss.SCSS_CLASS = None, child: scss.SCSS_CLASS = None) -> None:
        """
        The relationship method can create-relationship between the CHILD_CLASSES.
        # """

        if not isinstance(scss_class, scss.SCSS_CLASS):
            raise RELATIONSHIP_ERROR(f"This scss class:{scss_class} is not an scss class")

        if child and parent:
            raise RELATIONSHIP_ERROR(f"You can't bind 2 different things(child&parent)")

        if child:
            for scss_class_local in self._child_classes:
                try:
                    scss_class_local[scss_class]["child"] = child
                except:
                    continue

        #Todo: handle this parent logic
        if parent:
            for scss_class_local in self._child_classes:
                if scss_class_local[scss_class]:
                    scss_class_local[scss_class]["parent"] = child


    def render(self) -> str:
        """
        Render the whole group
        """
        render_group = ""

        for child_class_dict in self._child_classes:
            for scss_class, relationship in child_class_dict.items():
                render_group += scss_class.render()[:-1]

                for key, value in relationship.items():
                    if value != "":
                        render_group += value.render()
                render_group += "}" "\n"
        return render_group
