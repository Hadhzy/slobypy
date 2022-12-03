from __future__ import annotations

# Built-in
from typing import Self

# This project
from slobypy.errors.scss_errors import RelationshipError
import slobypy.react.scss_classes as scss


class SCSSGroupBase: # pylint: disable=too-few-public-methods
    def __init__(self, child_classes):
        self._child_classes = child_classes

    @property
    def child_classes(self) -> list[dict[scss.SCSSClass, dict]]:
        return self._child_classes


class SCSSGroup(SCSSGroupBase):
    """
    This class is representing a group of scss classes
    """
    GROUPS: list = [Self]  # all-groups

    def __init__(self, name):
        self.GROUPS.append(self)  # update the global group
        self.name = name  # get the name
        self._child_classes: list[dict[scss.SCSSClass]] = []  # store the local classes

        super().__init__(self._child_classes)  # pass the child_classes out

    def add(self, scss_class: scss.SCSSClass | list[scss.SCSSClass]):

        if isinstance(scss_class, scss.SCSSClass):
            self._child_classes.append(
                {scss_class: {"parent": "", "child": ""}})  # add a brand new scss_class to the local group

        if isinstance(scss_class, list):
            for scss_class_item in scss_class:
                self._child_classes.append(
                    {scss_class_item: {"parent": "", "child": ""}})  # add a brand new scss_class to the local group

    def relationship(self, scss_class: scss.SCSSClass, parent: scss.SCSSClass = None,
                     child: scss.SCSSClass = None) -> None:
        """
        The relationship method can create-relationship between the CHILD_CLASSES.
        """

        if not isinstance(scss_class, scss.SCSSClass):
            raise RelationshipError(f"This scss class:{scss_class} is not an scss class")

        if child and parent:
            raise RelationshipError("You can't bind 2 different things(child&parent)")

        if child:
            for scss_class_local in self._child_classes:
                try:
                    scss_class_local[scss_class]["child"] = child
                except:
                    continue

        # Todo: handle this parent logic
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
                render_group += scss_class.render()[:-1]  # cut the last brace

                for value in relationship.values():
                    if value != "":
                        render_group += "\n"
                        render_group += value.render()

                render_group += "}" "\n"

        return render_group

    def __iter__(self):
        start = 0
        end = len(self._child_classes)
        curr = start

        while curr < end:
            yield self._child_classes[curr]
            curr += 1
