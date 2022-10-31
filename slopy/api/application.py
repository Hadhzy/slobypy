# third-party
from fastapi import FastAPI


class SlopyAPI(FastAPI):
    """
    Get results from SoundCloud API and simplify them

    ### Arguments
    - search_term: The search term to search for.
    - kwargs: other keyword arguments passed to the `YTMusic.search` method.

    ### Returns
    - A list of simplified results (dicts)

    ### Anomalies
    - When using specific argument, blah blah blah
    """
    def __init__(self):
        super().__init__()