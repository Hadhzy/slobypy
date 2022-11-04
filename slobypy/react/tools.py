# This Project
from slobypy.react._types import url_type

# Third-Party
import validators
from validators import ValidationFailure


# FIXME: if the user does not pass out a "full" url just a simple endpoint
# TODO: Create a regex for this as the validators library is inconsistent
def url_checker(url: url_type) -> list[bool, url_type] | bool:
    """
    do the path_check here
    """
    slobypy_result = validators.url(url)

    if isinstance(slobypy_result, ValidationFailure):
        return False

    return [slobypy_result, url]
