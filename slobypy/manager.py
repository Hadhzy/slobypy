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
from slobypy.react.design import Design
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
    (path / "scss").mkdir(parents=True, exist_ok=True)

    # Todo: handle preprocessor
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

    component_base_path = Path(config["components"])  # the component folder
    component_paths = [component for component in component_base_path.iterdir() if
                       component.suffix == ".py"]  # get python files(inside components)

    scss_base_path = Path(config["scss"])
    scss_paths = [scss_file for scss_file in scss_base_path.iterdir() if scss_file.suffix == ".py"]

    modules.update(
        {component.resolve(): import_file(component) for component in component_paths})  # execute components files

    modules.update(
        {scss_path.resolve(): import_file(scss_path) for scss_path in scss_paths})

    # Attempt to run the app
    dash = SloDash(modules, config_path.parent)  # root folder(config parent)

    # Pash dash hook so that RPC updates can trigger UI changes
    SlApp.run(hooks=[dash], console=console,
              event_loop=dash.event_loop, tasks=dash.tasks, external_tasks=runtime_tasks, preprocessor=preprocessor,
              cwd=path.parent)


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
    def __init__(self, modules, path):
        self.rpc: RPC = SlApp.rpc  # Will be `None` until RPC started
        self.modules = modules

        self.path = path

        self.watch_callbacks = []

        self.tasks = [self.watch_root(path)]  # asyncio tasks
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        console.print("[blue]SlobyPy CLI v[cyan]1.0.0[/cyan] SloDash v[cyan]1.0.0[/cyan][/]\n")

    # noinspection PyProtectedMember
    async def watch_scss_added(self, path: Path):

        if (self.path / 'scss').resolve() in path.parents:
            return []

    # noinspection PyProtectedMember
    async def watch_scss_modified(self, path: Path):
        if (self.path / "scss").resolve() in path.parents:
            for scss_class in Design.get_registered_classes():
                if Path(scss_class["source_path"]) == path:
                    Design._REGISTERED_CLASSES.remove(scss_class)

        return []

    # noinspection PyProtectedMember
    async def watch_component_added(self, path: Path):
        if (self.path / 'components').resolve() in path.parents:
            return [component["uri"] for component in SlApp._components if
                    component["source_path"] == path]
        return []

    # noinspection PyProtectedMember
    async def watch_component_modified(self, path: Path):
        routes = []
        if (self.path / 'components').resolve() in path.parents:
            for component in SlApp._components.copy():
                if str(component["source_path"].resolve()) == str(path.resolve()):
                    SlApp._components.remove(component)
                    routes.append(component["uri"])

        return routes

    # noinspection PyProtectedMember
    async def watch_root(self, path):
        console.log(f"Watching {str(path.resolve())} for changes")
        async for changes in awatch(str(path.resolve())):
            for change in changes:
                path = Path(change[1])
                routes = []
                if path.suffix == ".py":
                    if change[0]._value_ == 1:  # Added
                        self.modules.update({path.resolve(): import_file(path)})
                        for callback in self.watch_callbacks:
                            routes.extend(await callback["added"](path))
                    elif change[0]._value_ == 2:  # Modified
                        for callback in self.watch_callbacks:
                            routes.extend(await callback["modified"](path))

                        # Reload the module
                        self.modules[path.resolve()] = reload(self.modules[path.resolve()])
                    else:
                        # Deleted
                        for callback in self.watch_callbacks:
                            routes.extend(await callback["removed"](path))
                        del self.modules[path.resolve()]

                    for callback in self.watch_callbacks:
                        if callback["changes_done"] is not None:
                            await callback["changes_done"](path)

                    await self.rpc.hot_reload_routes(routes)

    # noinspection PyMethodMayBeStatic
    async def on_start(self, host, port):
        self.watch_callbacks = [
            {
                "added": self.watch_component_added,
                "modified": self.watch_component_modified,
                "removed": self.watch_component_modified,
                "changes_done": None
            },
            {
                "added": self.watch_scss_added,
                "modified": self.watch_scss_modified,
                "removed": self.watch_scss_modified,
                "changes_done": self.rpc.reload_all_css,
            }
        ]

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
