# Built-in
import asyncio
import json
import sys
import importlib.util
import importlib.machinery
import importlib.abc
import socket
import urllib.request
import urllib.error

from pathlib import Path
from importlib import reload

# Third-Party
import typer

from watchfiles import awatch

# This project
from slobypy.app import SlApp
from slobypy.rpc import RPC
from slobypy._templates import *

# Rich
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer()
console = Console()


@app.command()
def generate(path: str, overwrite: bool = False):
    # Used to generate a new project
    path = Path(path)
    # Check if path is empty
    if path.is_file():
        typer.echo("Path is a file, not a directory")
        return

    if path.exists() and not overwrite:
        if any(path.iterdir()):
            typer.echo("Path is not empty")
            return

    # Create directories if they don't exist
    path.mkdir(parents=True, exist_ok=True)  # exist_ok mutes the error if the directory already exists
    (path / "components").mkdir(parents=True, exist_ok=True)

    with open(path / "sloby.config.json", "w") as f:
        f.write(CONFIG)

    with open(path / "app.py", "w") as f:
        f.write(MAIN_FILE)

    with open((path / "components") / "example_component.py", "w") as f:
        f.write(COMPONENT_FILE)


@app.command()
def run(config: str = "sloby.config.json") -> None:
    """
        This function is used to run the websockets.

        ### Arguments
        - config: default value | main.py

        ### Returns
        - None
    """

    # Attempt to import the file using importlib
    config_path = Path(config)

    # Read config_path with json
    with open(config_path, "r") as f:
        config = json.load(f)

    path = Path(config["main"])  # main.py
    runtime_tasks = config["runtime_tasks"]

    preprocessor = None
    if config.get("preprocessor", None) is not None:
        if config["preprocessor"]:
            preprocessor = import_file(Path(config["preprocessor"]))

    # Modules are used to keep track of ALL imported modules
    modules = {path.resolve: import_file(path)}  # execute the main.py

    component_path = path.parent / config["components"]
    component_paths = [component for component in component_path.iterdir() if
                       component.suffix == ".py"]  # get python files

    modules.update(
        {component.resolve(): import_file(component) for component in component_paths})  # execute components files

    # Attempt to run the app
    dash = SloDash(modules, component_path)

    # Pash dash hook so that RPC updates can trigger UI changes
    SlApp.run(hooks=[dash], console=console,
              event_loop=dash.event_loop, tasks=dash.tasks, external_tasks=runtime_tasks, preprocessor=preprocessor)


class ModuleFinder(importlib.abc.MetaPathFinder):

    def __init__(self, path_map: dict):
        self.path_map = path_map

    def find_spec(self, fullname, path, target=None):
        if not fullname in self.path_map:
            return None
        return importlib.util.spec_from_file_location(fullname, self.path_map[fullname])

    def find_module(self, fullname, path):
        return None  # No need to implement, backward compatibility only


def import_file(path: Path):
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path.resolve())
        module = importlib.util.module_from_spec(spec)
        sys.meta_path.append(ModuleFinder({path.stem: str(path.resolve())}))
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        return module
    except AttributeError:
        typer.echo("File not found")
        return


class SloDash:
    def __init__(self, modules, source_path):
        self.rpc: RPC = SlApp.rpc  # Will be `None` until RPC started
        self.modules = modules
        self.source_path = source_path
        self.tasks = [self.watch_files(self.source_path)]
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        console.print("[blue]SlobyPy CLI v[cyan]1.0.0[/cyan] SloDash v[cyan]1.0.0[/cyan][/]\n")

    # noinspection PyProtectedMember
    async def watch_files(self, path: Path):
        # Watch the files for changes
        console.log(f"Watching files at {str(path.resolve())}...")
        async for changes in awatch(str(path.resolve())):
            for change in changes:
                path = Path(change[1])
                routes = []
                if path.suffix == ".py":
                    if change[0]._value_ == 1:  # Added
                        self.modules.update({path.resolve(): import_file(path)})
                        routes = [component["uri"] for component in SlApp._components if
                                  component["source_path"] == path]
                    elif change[0]._value_ == 2:  # Modified
                        for component in SlApp._components.copy():
                            if str(component["source_path"].resolve()) == str(path.resolve()):
                                SlApp._components.remove(component)
                                routes.append(component["uri"])

                        # Reload the module
                        module = self.modules[path.resolve()]
                        self.modules[path.resolve()] = reload(module)
                    else:
                        # Deleted
                        del self.modules[path.resolve()]
                        for component in SlApp._components:
                            if component["source_path"] == path:
                                SlApp._components.remove(component)
                                routes.append(component["uri"])

                    await self.rpc.hot_reload_routes(routes)

    # noinspection PyMethodMayBeStatic
    async def on_start(self, host, port):
        grid = Table.grid(padding=(0, 3))
        grid.add_column()
        grid.add_column(justify="left")
        grid.add_row("> Local RPC:", f"http://localhost:{port}")
        grid.add_row("> Network RPC:", f"http://{socket.gethostbyname(socket.gethostname())}:{port}")
        try:
            external_ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
        except urllib.error.URLError:
            external_ip = "Unknown"
        grid.add_row("> Network RPC:", f"http://{external_ip}:{port} :warning:")

        console.print(Panel(
            grid,
            expand=False,
            border_style="blue")
        )

        console.print("Waiting for connection from Sloby...\n", style="yellow")


def start_typer():
    app()


if __name__ == "__main__":
    start_typer()
