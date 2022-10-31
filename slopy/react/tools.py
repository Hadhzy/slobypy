# this project
from slopy.react._types import url_type
# third party
from urllib.parse import urlparse


#FIXME: for some reasons everything is true: https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not
def url_checker(url: url_type):
    """
    do the path_check here
    """
    before_url = "http://localhost:3000/"
    slopy_url = before_url + url
    try:
        slopy_result = urlparse(slopy_url)
        return all([slopy_result.scheme, slopy_result.netloc])
    except:
        return False
