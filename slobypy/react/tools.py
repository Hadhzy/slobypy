# this project
from slobypy.react._types import url_type
# third party
import validators
from validators import ValidationFailure


#FIXME: if the user does not pass out a "full" url just a simple endpoint
def url_checker(url: url_type) -> list[bool, url_type] | bool:
    """
    do the path_check here
    """
    slobypy_result = validators.url(url)

    if isinstance(slobypy_result, ValidationFailure):
        return False

    return [slobypy_result, url]



