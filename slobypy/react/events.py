# This Project
from slobypy.rpc import Event


class EventHandler:
    """
        description needed

    """

    @staticmethod
    def listen(event: Event = None):
        def listen_decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                print(event)
                return result

            return wrapper

        return listen_decorator
