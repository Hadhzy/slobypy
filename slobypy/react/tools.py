# This Project
from slobypy.react._types import url_type

# Third-Party
from urllib.parse import urlparse


def url_checker(url: url_type) -> str | bool:
    """
     ### Arguments
    - url: The url of the component

    ### Returns
    url: if the url is valid
    False: if the url is not valid
    """

    slobypy_result = urlparse(url)

    if slobypy_result.path and slobypy_result.scheme is not True:
        return url

    return False