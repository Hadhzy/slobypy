# pylint: disable=protected-access

import random
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from pathlib import Path
from typing import Callable, Awaitable, Any, List, Coroutine, Type

import asyncio
import json

from dataclasses import dataclass

import websockets.exceptions
from rich.console import Console
from websockets import serve  # pylint: disable=no-name-in-module
from websockets.legacy.server import WebSocketServerProtocol

from .react.design import Design
# This project
from .react.component import AppComponent

class RPC:
    CURRENT_VERSION = '0.A1'
    """
    The RPC class is used to communicate with the React frontend and remotely call events and methods

    ### Arguments
    - None

    ### Returns
    - None
    """

    def __init__(self, app,
                 host: str = "localhost",
                 port: int = 8765,
                 hooks: list = None,
                 console: Console = None,
                 event_loop: AbstractEventLoop = None,
                 tasks: List[Coroutine] = None,
                 external_tasks: List[str] = None,
                 preprocessor=None,
                 cwd: Path = None,
                 pre_rendered=None):
        self.css_preprocessor: Callable[[], Awaitable[Path]] = None

        if tasks is None:
            tasks = []
        if hooks is None:
            hooks = []
        self.app = app
        self.hooks = hooks
        self.console = console
        self.pre_rendered = pre_rendered or []
        if event_loop is None:
            event_loop = asyncio.get_event_loop()
        self.event_loop = event_loop
        asyncio.set_event_loop(self.event_loop)
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.tasks = tasks
        self.external_tasks = external_tasks
        self.preprocessor = preprocessor  # the module
        self.cwd = cwd

        self.ws = None  # pylint: disable=invalid-name
        self.conn = []

        for hook in hooks:
            hook.rpc = self

        asyncio.run(self.run(host, port))

    async def run(self, host: str, port: int):
        """
        Runs the event loop

        ### Arguments
        - None

        ### Returns
        - None
        """
        if self.external_tasks:
            await asyncio.create_subprocess_shell(*self.external_tasks)

        preprocessor_tasks = []
        if self.preprocessor:
            processors = await self.preprocessor.init(self, self.cwd)
            self.css_preprocessor = processors.get("process_css", None)
            preprocessor_tasks = processors.get("tasks", [])

        futures = []
        for task in preprocessor_tasks:
            futures.append(asyncio.create_task(task))

        await asyncio.gather(*self.tasks, *futures, self.create_ws(self._handle_ws, host, port))
        pending = asyncio.all_tasks()
        self.event_loop.run_until_complete(asyncio.gather(*pending))

    async def send_hook(self, name: str, *args, **kwargs):
        """
        Calls any hooks that are registered with the RPC (e.g. SloDash)

        ### Arguments
        - name (str): The name of the hook to call
        - *args: The arguments to pass to the hook
        - **kwargs: The keyword arguments to pass to the hook

        ### Returns
        - None
        """
        for hook in self.hooks:
            try:
                await getattr(hook, name)(*args, **kwargs)
            except AttributeError:
                continue

    async def log(self, data: Any):
        """
        Logs data to the console

        ### Arguments
        - data (Any): The data to log to the console

        ### Returns
        - None
        """
        if self.console:
            self.console.log("[black on grey37] INFO [/]", data)

    async def warn(self, data: Any):
        """
        Logs a warning to the console

        ### Arguments
        - data (Any): The data to log to the console

        ### Returns
        - None
        """
        if self.console:
            self.console.log("[black on yellow] WARN [/]", data)

    async def error(self, data: Any):
        """
        Logs an error to the console

        ### Arguments
        - data (Any): The data to log to the console

        ### Returns
        - None
        """
        if self.console:
            self.console.log("[black on red] ERROR [/]", data)

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
        await self.send_hook("on_start", host, port)
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
        await self.send_hook("on_connect", conn)
        await self.log(f"Received Sloby connection from {':'.join(map(str, conn.remote_address))}")
        await self.listen(conn)

    async def listen(self, conn: WebSocketServerProtocol):
        """
        Listens for messages from the React frontend

        ### Arguments
        - None

        ### Returns
        - None
        """
        try:
            async for msg in conn:
                data = json.loads(msg)
                await self.handle_event(conn, data)
        except websockets.exceptions.ConnectionClosedError:
            await self.send_hook("on_disconnect", conn)
            try:
                conn_id = conn._sloby_id
                self.conn[conn._sloby_id - 1]["_internal_heartbeat"].cancel()
            except AttributeError:
                conn_id = "Unknown"
            await self.warn(f"Lost Sloby connection from {':'.join(map(str, conn.remote_address))}, id: {conn_id}")

    async def handle_event(self, conn: WebSocketServerProtocol, data: dict):
        """
        Handles the event sent from the React frontend

        ### Arguments
        - data (dict): The data sent from the React frontend

        ### Returns
        - None
        """
        if data["type"] == "identify":
            await self.identify(conn, data["data"])
        elif data["type"] == "heartbeat":
            await self.heartbeat(conn)
        elif data["type"] == "new_shard":
            await self.new_shard(conn, data["data"])
        elif data["type"] == "remove_shard":
            self.conn[conn._sloby_id - 1]["shards"].pop(str(data["data"]["id"]))
        elif data["type"] == "shard_event":
            await self.shard_event(conn, data["data"])
        elif data["type"] == "get_route":
            await self.render_shard(conn, data["data"])

    async def send(self, conn: WebSocketServerProtocol, data: dict):
        """
        Sends data to the React frontend

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection
        - data (dict): The data to send to the React frontend

        ### Returns
        - None
        """
        await conn.send(json.dumps(data))

    async def wait_for_hearbeat(self, conn: WebSocketServerProtocol):
        """
        Waits for a heartbeat from the React frontend

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection

        ### Returns
        - None
        """
        async def internal_wait(latency):
            await asyncio.wait_for(event.wait(), timeout=(interval + latency) / 1000)
            event.clear()
            await self.send(conn, {
                "type": "heartbeatACK",
                "data": None,
                "sequence": None,
            })

        event = self.conn[conn._sloby_id - 1]["heartbeat"]
        interval = self.conn[conn._sloby_id - 1]["heartbeat_interval"]

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

    async def heartbeat(self, conn: WebSocketServerProtocol):
        """
        Handles the heartbeat from the React frontend

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection

        ### Returns
        - None
        """
        self.conn[conn._sloby_id - 1]["heartbeat"].set()

    async def pre_rendered_send(self, conn):
        """Used to render the static components"""
        for component in self.pre_rendered:
            await self.send(conn, {"route": component["uri"], "html": await self.get_route(component["uri"])})


    async def identify(self, conn: WebSocketServerProtocol, data: dict):
        """
        Identifies the React frontend's websocket

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection
        - data (dict): The data sent from the React frontend

        ### Returns
        - None
        """
        conn._sloby_id = len(self.conn) + 1
        conn._sloby_loaded_initial_css = False

        self.conn.append({
            "id": conn._sloby_id,  # Integer used to identify the connection, is used if a connection is lost,
            "conn": conn,  # The websocket connection
            "client": data["client"],  # String used to identify the client incase it's not Sloby
            "max_shards": data["max_shards"],  # Maximum number of requests the socket can handle
            "shards": data["shards"],  # Current shards on socket
            "heartbeat_interval": data["heartbeat_interval"],  # Interval in milliseconds to send heartbeat
            "heartbeat": asyncio.Event(),  # Event to acknowledge heartbeat
        })

        await self.pre_rendered_send(conn)
        await self.send_hook("on_identify", conn, data)
        await self.log(
            f"Identified Sloby connection from {':'.join(map(str, conn.remote_address))}, id: {conn._sloby_id}, "
            f"client: [cyan]{data['client']}[/cyan], max_shards: {data['max_shards']}")

        await self.send(conn, {
            "type": "ready",
            "data": {
                "id": conn._sloby_id,
            },
            "sequence": random.randint(1000, 9999),  # Sequence number used to identify lost packets
        })

        # Create task to watch for heartbeat
        self.conn[conn._sloby_id - 1]["_internal_heartbeat"] = asyncio.ensure_future(self.wait_for_hearbeat(conn))

    async def new_shard(self, conn: WebSocketServerProtocol, data: dict):
        """
        Handles a new shard request from the React frontend

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection
        - data (dict): The data sent from the React frontend

        ### Returns
        - None
        """
        self.conn[conn._sloby_id - 1]["shards"][str(data["id"])] = data
        await self.send_hook("on_new_shard", conn, data)
        await self.log(f"New shard #{data['id']} on connection #{conn._sloby_id}, route: {data['route']}")
        # Serve initial route
        if conn._sloby_loaded_initial_css:
            await self.reload_css(conn)
        await self.render_shard(conn, data)

    async def render_shard(self, conn: WebSocketServerProtocol, data: dict):
        """
        Renders a shard to the React frontend

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection
        - data (dict): The data sent from the React frontend

        ### Returns
        - None
        """
        start_time = datetime.now()
        self.conn[conn._sloby_id - 1]["shards"][str(data["id"])]["route"] = data["route"]
        self.conn[conn._sloby_id - 1]["shards"][str(data["id"])]["last_render"] = data
        await self.update_shard_data(conn, data["id"], await self.get_route(data["route"]))
        await self.send_hook("on_render_shard", conn, data)
        await self.log(f"Rendered shard #{data['id']} on connection #{conn._sloby_id}, route: {data['route']} in "
                       f"{int(round((datetime.now() - start_time).total_seconds(), 3) * 1000)}ms")

    async def update_shard_data(self, conn: WebSocketServerProtocol, shard_id, html: str):
        """
        Updates the html data of a shard

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection
        - shard_id (int): The id of the shard to update
        - html (str): The html to update the shard with

        ### Returns
        - None
        """
        await self.send(conn, {
            "type": "update_shard_data",
            "data": {
                "id": shard_id,
                "html": html
            },
            "sequence": random.randint(1000, 9999),
        })

    async def shard_event(self, conn: WebSocketServerProtocol, data: dict):
        """
        Handles a shard event from the React frontend

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection
        - data (dict): The data sent from the React frontend

        ### Returns
        - None
        """
        pass

    async def get_route(self, route):
        """
        Gets the html of a route

        ### Arguments
        - route (str): The route to get the html of

        ### Returns
        - str: The full html data of the route
        """
        return self.app._render(route=route)

    async def reload_all_css(self, *args, **kwargs):
        """
        Reloads all css on all connections

        ### Arguments
        - None

        ### Returns
        - list: An empty list (Used for SloDash purposes)
        """
        for connection in self.conn:
            await self.reload_css(connection["conn"])

        return []

    async def reload_css(self, conn: WebSocketServerProtocol):
        """
        Reloads the css on a connection

        ### Arguments
        - conn (WebSocketServerProtocol): The websocket connection

        ### Returns
        - None
        """
        await self.send(conn, {
            "type": "reload_css",
            "data": {
                "css": await self.get_css(),
            },
            "sequence": random.randint(1000, 9999),
        })

    async def get_css(self):
        """
        Renders the CSS in the application

        ### Arguments
        - None

        ### Returns
        - str: The full css data of the application
        """
        if self.css_preprocessor is None:
            # When no preprocessor, fallback to default
            return "\n".join([scss_data["scss_class"].render() for scss_data in Design._REGISTERED_CLASSES])
        else:
            return (await self.css_preprocessor()).read_text()

    #noinspection PyProtectedMember
    #noinspection PyMethodMayBeStatic
    async def check_app(self, shard_route, routes):
        if AppComponent._components:
            for app_component in AppComponent._components:
                if app_component["uri"] == shard_route:
                    return True
            else:
                return
        else:
            return shard_route in routes




    async def hot_reload_routes(self, routes: list):
        """
        Hot reloads routes on all connections

        ### Arguments
        - routes (list): The routes to hot reload

        ### Returns
        - None
        """
        # Re-render all RPC shards on those routes
        print("hot reload routes", routes)
        routes = routes or []
        print(set(routes))
        for connection in self.conn:
            for shard in connection["shards"].values():

                if await self.check_app(shard["route"], list(set(routes))):
                    # Replay last-render (same route)
                    await self.render_shard(connection["conn"], shard["last_render"])


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
