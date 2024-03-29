"""Contains custom exceptions for the react module."""


class URIError(Exception):
    """URIError is raised when the uri is not valid"""


class NotRegistered(Exception):
    pass


class NotValidComponent(Exception):
    pass