"""Contains custom exceptions for the SCSS-based modules"""


class PropertyKeyError(Exception):
    """PropertyKeyError is raised when the property key is not valid"""
    pass


class NotSame(Exception):
    """NotSame is raised when the two values are not the same"""
    pass


class RelationshipError(Exception):
    """RelationshipError is raised when the relationship is not valid"""
    pass


class NoName(Exception):
    """NoName is raised when the name is not valid"""
    pass
