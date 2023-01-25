"""General utilities used throughout the react sub-package"""
from urllib.parse import urlparse

from ..errors.react_errors import URIError

__all__: tuple[str, ...] = ("uri_checker",)


def uri_checker(uri: str | None = None) -> str:
    """
     ### Arguments
    - uri: The uri of the component

    ### Returns
    uri: if the uri is valid
    error: if the uri is not valid
    """
    if uri is None:
        return ""
    slobypy_result = urlparse(uri)

    if slobypy_result.path and slobypy_result.scheme is not True:
        return uri

    raise URIError("Not valid uri")


uri_checker()
