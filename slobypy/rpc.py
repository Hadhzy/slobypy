import datetime
import random
from typing import Callable, Awaitable, Any

import asyncio
import json

from dataclasses import dataclass
from websockets import serve  # pylint: disable=no-name-in-module
from websockets.legacy.server import WebSocketServerProtocol


class RPC:
    CURRENT_VERSION = '0.A1'
    """
    The RPC class is used to communicate with the React frontend and remotely call events and methods

    ### Arguments
    - None

    ### Returns
    - None
    """

    def __init__(self):
        self.event_loop = asyncio.get_event_loop()
        self.ws = None  # pylint: disable=invalid-name
        self.conn = []

        self.event_loop.run_until_complete(self.create_ws(self._handle_ws))

    async def create_ws(self,
                        ws_handler: Callable[[WebSocketServerProtocol], Awaitable[Any]],
                        host: str = "localhost",
                        port: int = 8765):
        """
        Creates a websocket connection to the React frontend

        ### Arguments
        - ws_handler (callable): The function to handle the websocket connection
        - host (str): The host to connect to
        - port (int): The port to connect to

        ### Returns
        - None
        """
        self.ws = await serve(ws_handler, host, port)
        await self.ws.serve_forever()

    async def _handle_ws(self, conn: WebSocketServerProtocol):
        """
        Handles the websocket connection

        ### Arguments
        - ws (websockets): The websocket connection

        ### Returns
        - None
        """
        await self.listen(conn)

    async def listen(self, conn):
        """
        Listens for messages from the React frontend

        ### Arguments
        - None

        ### Returns
        - None
        """
        async for msg in conn:
            data = json.loads(msg)
            print(data)
            await self._handle_event(conn, data)

    async def _handle_event(self, conn, data: dict):
        """
        Handles the event sent from the React frontend

        ### Arguments
        - data (dict): The data sent from the React frontend

        ### Returns
        - None
        """
        if data["type"] == "identify":
            await self._identify(conn, data["data"])
        elif data["type"] == "heartbeat":
            await self._heartbeat(conn)

    async def send(self, conn, data: dict):
        """
        Sends data to the React frontend

        ### Arguments
        - data (dict): The data to send to the React frontend

        ### Returns
        - None
        """
        await conn.send(json.dumps(data))

    async def _wait_for_hearbeat(self, conn):
        async def internal_wait(latency):
            await asyncio.wait_for(event.wait(), timeout=(interval + latency) / 1000)
            event.clear()
            await self.send(conn, {
                "type": "heartbeatACK",
                "data": None,
                "sequence": None,
            })

        event = self.conn[conn.id - 1]["heartbeat"]
        interval = self.conn[conn.id - 1]["heartbeat_interval"]

        while True:
            try:
                # Up to 80ms of latency is supported
                await internal_wait(80)
            except TimeoutError:
                # Ask for a heartbeat, client must respond with a heartbeat within 100ms
                await self.send(conn, {"type": "heartbeat", "data": None, "sequence": None})
                try:
                    await internal_wait(100)
                except TimeoutError:
                    # Ask for reconnect and kill connection
                    await self.send(conn, {"type": "reconnect", "data": None, "sequence": None})
                    await conn.close()
                    break

    async def _heartbeat(self, conn):
        """
        Handles the heartbeat from the React frontend

        ### Arguments
        - None

        ### Returns
        - None
        """
        self.conn[conn.id - 1]["heartbeat"].set()

    async def _identify(self, conn, data: dict):
        """
        Identifies the React frontend's websocket

        ### Arguments
        - data (dict): The data sent from the React frontend

        ### Returns
        - None
        """
        conn.id = data["id"]

        self.append = self.conn.append({
            "id": data["id"],  # Integer used to identify the connection, is used if a connection is lost,
            "conn": conn,  # The websocket connection
            "client": data["client"],  # String used to identify the client incase it's not Sloby
            "max_shards": data["max_shards"],  # Maximum number of requests the socket can handle
            "shards": data["shards"],  # Current shards on socket
            "heartbeat_interval": data["heartbeat_interval"],  # Interval in milliseconds to send heartbeat
            "heartbeat": asyncio.Event(),  # Event to acknowledge heartbeat
        })

        await self.send(conn, {
            "type": "ready",
            "data": None,
            "sequence": random.randint(1000, 9999),  # Sequence number used to identify lost packets
        })

        # Create task to watch for heartbeat
        self.event_loop.create_task(self._wait_for_hearbeat(conn))


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
