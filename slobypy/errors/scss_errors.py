"""Contains custom exceptions for the SCSS-based modules"""


class PropertyKeyError(Exception):
    """PropertyKeyError is raised when the property key is not valid"""


class NotSame(Exception):
    """NotSame is raised when the two values are not the same"""


class RelationshipError(Exception):
    """RelationshipError is raised when the relationship is not valid"""


class NoName(Exception):
    """NoName is raised when the name is not valid"""
