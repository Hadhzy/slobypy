# This Project
from slobypy.react._react_types import uri_type
from slobypy.errors.react_errors import URI_ERROR
# Third-Party
from urllib.parse import urlparse


def uri_checker(uri: uri_type) -> str | bool:
    """
     ### Arguments
    - url: The url of the component

    ### Returns
    url: if the url is valid
    False: if the url is not valid
    """

    slobypy_result = urlparse(uri)

    if slobypy_result.path and slobypy_result.scheme is not True:
        return uri

    raise URI_ERROR("Not valid url")
