# This project

# Built-in
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from slobypy.react.scss_classes import SCSS_CLASS


class SCSS_GROUP_BASE:
    def __init__(self, child_classes):
        self._child_classes = child_classes


    @property
    def child_classes(self) -> "list[dict[SCSS_CLASS, dict]]":
        return self._child_classes


class SCSS_GROUP(SCSS_GROUP_BASE):
    """
    This class is representing a group of scss classes
    """
    GROUPS: list = [Self]

    def __init__(self, name):
        self.GROUPS.append(self)  # update the global group
        self.name = name  # get the name
        self._child_classes: "list[dict[SCSS_CLASS]]" = []  # store the local classes

        super().__init__(self._child_classes)


    def add(self, scss_class: "SCSS_CLASS"):
        self._child_classes.append({scss_class: {"parent": "", "child": ""}})  # add a brand new scss_class to the local group

    def relationship(self, scss_class: "SCSS_CLASS", parent: "SCSS_CLASS" = None, child: "SCSS_CLASS" = None) -> None:
        """
        The relationship method can create-relationship between the CHILD_CLASSES.
        # """
        #
        # if isinstance(scss_class, SCSS_CLASS) and scss_class in self._child_classes:
        #     for class_dict in self._child_classes:
        #         class_dict[scss_class] = {"parent": parent if isinstance(parent, SCSS_CLASS) else "", "child": child if isinstance(child, SCSS_CLASS) else scss_class.child)}
        #
        # elif isinstance(scss_class, SCSS_CLASS) and scss_class not in self._child_classes:
        #     if isinstance(parent, SCSS_CLASS):
        #         self._child_classes.append(parent)
        #
        #     self._child_classes.append({scss_class: {"parent": parent if isinstance(parent, SCSS_CLASS) else "", "child": child if isinstance(child, SCSS_CLASS) and child.child != "" else ""}})
        pass

    def render(self) -> str:
        """
        Render the whole group
        """
        render_group = ""

        for child_class_dict in self._child_classes:
            for scss_class, value in child_class_dict.items():

                render_group += scss_class.render()

        return render_group
