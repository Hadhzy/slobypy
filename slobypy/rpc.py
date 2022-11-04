from dataclasses import dataclass


class RPC:
    """
    The RPC class is used to communicate with the React frontend and remotely call events and methods

    ### Arguments
    - None

    ### Returns
    - None
    """

    pass


@dataclass
class Event:
    """
    This class is used to create events that can be emitted by the `slobypy` library. This class will contain
    metadata and information about the event that was emitted.

    ### Arguments
    - name: The name of the component that emitted the event
    - type: The type of event that was emitted
    - time: The time that the event was emitted (according to React)
    - data: The data that was emitted with the event

    ### Returns
    - None
    """

    name: str
    type: str
    time: int
    data: dict
