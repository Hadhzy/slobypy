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
from textual.events import Key

from watchfiles import awatch

# This project
from slobypy.app import SlApp  # type: ignore
from slobypy.react.design import Design
from slobypy.rpc import RPC
from slobypy._templates import *
from slobypy.react.component import AppComponent
from slobypy.react.tools import SloDebugHandler
# Rich
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Textual
from textual.app import App, ComposeResult
from textual.widgets import Footer, Static
from textual.widget import Widget
from textual.reactive import reactive
from textual.binding import Binding

app = typer.Typer()
console = Console()


# noinspection PyArgum
# entList
@app.command()
def generate(path: Path, overwrite: bool = False, no_preprocessor=False):
    """
    Generate a new project.

    ### Arguments
    - path (str): The path to the project.
    - overwrite (bool): Overwrite the project if it already exists.
    - no_preprocessor (bool): Don't use a preprocessor.

    ### Returns
    - None
    """

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
    (path / "components").mkdir(parents=True, exist_ok=True)  # type: ignore
    (path / "scss").mkdir(parents=True, exist_ok=True)

    NEW_CONFIG = CONFIG.substitute(preprocessor=f'"preprocessor": "preprocessor.py",')
    with open(path / "sloby.config.json", "w") as f:
        f.write(NEW_CONFIG)

    with open(path / "app.py", "w") as f:
        f.write(MAIN_FILE)

    with open((path / "components") / "example_component.py", "w") as f:
        f.write(COMPONENT_FILE)

    if no_preprocessor is not True:
        slo_text = SloText(path)
        slo_text.run()

        selected_preprocessor = slo_text.get_selected_preprocessor()[0]
        library_start = slo_text.get_selected_preprocessor()[1]
        NEW_PREPROCESSOR = PREPROCESSOR.substitute(library=selected_preprocessor,
                                                   library_start=library_start)

        if selected_preprocessor == "tailwind":
            # Create tailwind dependencies here
            pass
        elif selected_preprocessor == "sass":
            # Create sass dependencies here
            pass

        elif selected_preprocessor == "boostrap":
            # Create boostrap dependencies here
            pass


        with open((path / "preprocessor.py"), "w") as f:
            if no_preprocessor is not True:
                f.write(NEW_PREPROCESSOR)


@app.command()
def SloBug():
    """Used to help the user debug the code"""
    SloInspector().run()  # Run the Inspection ui


@app.command()
def generate_delete(path: Path):
    """Used to remove the generated files"""
    if path.exists():
        if any(path.iterdir()) is False:
            typer.echo("The path is empty")

    config_file = Path(path / "sloby.config.json")
    app_file = Path(path / "app.py")
    example_component = Path(path / "components" / "example_component.py")
    preprocessor = Path(path / "preprocessor.py")

    deleted_files = [config_file, app_file, example_component, preprocessor]

    for file in deleted_files:
        try:
            file.resolve().unlink()
            console.print(f"Deleted file:{file}", style="red")
        except:
            console.print(f"Can't remove:{file}", style="yellow")

    console.print("Successfully delete!", style="magenta")


@app.command()
def run(config: str = "sloby.config.json", slo_bug: Path = "") -> None:
    """
    This function is used to run the websockets.

    ### Arguments
    - config: default value | main.py

    ### Returns
    - None
    """
    json_path = Path(slo_bug)

    if slo_bug:  # if slo_bug defined
        SloDebugHandler.set_path(json_path)  # !May be duplicated files if it's not match

        if SloDebugHandler.analyse():  # if cls.path already defined
            console.print(f"[blue underline]There is already a handler json file")
        else:  # if not
            console.log(f"[blue underline]Successfully created: {json_path.absolute()}")

    # Attempt to import the file using importlib
    config_path = Path(config)

    # Read config_path with json
    with open(config_path, "r") as f:
        config = json.load(f)

    path = Path(config["main"])  # app.py
    runtime_tasks = config["runtime_tasks"]

    preprocessor = None
    if config.get("preprocessor", None) is not None:
        if config["preprocessor"]:
            preprocessor = import_file(Path(config["preprocessor"]))

    # Modules are used to keep track of ALL imported modules
    modules = {path.resolve(): import_file(path)}  # execute the app.py (user-provided)

    component_base_path = Path(config["components"])  # the component folder
    component_paths = [component for component in component_base_path.iterdir() if
                       component.suffix == ".py"]  # get python files(inside components)

    scss_base_path = Path(config["scss"])
    scss_paths = [scss_file for scss_file in scss_base_path.iterdir() if scss_file.suffix == ".py"]

    modules.update(
        {component.resolve(): import_file(component) for component in component_paths})  # execute components files

    modules.update(
        {scss_path.resolve(): import_file(scss_path) for scss_path in scss_paths})  # execute scss files
    # Attempt to run the app
    dash = SloDash(modules, config_path.parent)  # root folder(config parent)

    # Pash dash hook so that RPC updates can trigger UI changes
    SlApp.run(hooks=[dash], console=console,
              event_loop=dash.event_loop, tasks=dash.tasks, external_tasks=runtime_tasks, preprocessor=preprocessor,
              cwd=path.parent, pre_rendered=dash.pre_rendered)


class ModuleFinder(importlib.abc.MetaPathFinder):

    def __init__(self, path_map: dict):
        self.path_map = path_map

    def find_spec(self, fullname, path, target=None):
        """Find the module spec for a module."""
        if not fullname in self.path_map:
            return None
        return importlib.util.spec_from_file_location(fullname, self.path_map[fullname])

    def find_module(self, fullname, path):
        """Find the module given the fullname and path, only for backwards compatibility"""
        return None  # No need to implement, backward compatibility only


def import_file(path: Path):
    """
    Import a file using importlib.

    ### Arguments
    - path (Path): The path to the file.

    ### Returns
    - module (Module): The imported module.
    """
    try:
        spec = importlib.util.spec_from_file_location(path.stem, path.resolve())
        module = importlib.util.module_from_spec(spec)
        sys.meta_path.append(ModuleFinder({path.stem: str(path.resolve())}))
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        print("execute something!")
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
        self.pre_rendered: list = []

        self.tasks = [self.watch_root(path)]  # asyncio tasks
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)

        console.print("[blue]SlobyPy CLI v[cyan]1.0.0[/cyan] SloDash v[cyan]1.0.0[/cyan][/]\n")

    async def preprocessor_exist(self) -> bool:
        """Check if preprocessor exists"""
        if (self.path / "preprocessor.py").exists():
            return True
        return False

    # noinspection PyProtectedMember
    async def watch_scss_added(self, path: Path) -> list:
        """Hook that is called when a scss file is added"""
        if (self.path / 'scss').resolve() in path.parents:
            return []

    # noinspection PyProtectedMember
    async def watch_scss_modified(self, path: Path) -> list:
        """Hook that is called when a scss file is modified"""
        if (self.path / "scss").resolve() in path.parents:
            for scss_class in Design.get_registered_classes():
                if Path(scss_class["source_path"]) == path:
                    Design._REGISTERED_CLASSES.remove(scss_class)

        return []

    def check_pre_rendered(self, component) -> str | None:
        """Used to check if the component is pre-rendered or not"""
        if component["static"] is True:
            self.pre_rendered.append(component)
            return
        uri = component["uri"]
        return uri

    # noinspection PyProtectedMember
    async def watch_component_added(self, path: Path) -> list | list[str]:
        """Hook that is called when a component file is added"""
        if not AppComponent._components:
            if (self.path / 'components').resolve() in path.parents:
                return [(self.check_pre_rendered(component),

                        SloDebugHandler.add_json(base_key="registered_components", sub_key=component["uri"], add_item=component))

                        for component in SlApp._components if
                        component["source_path"] == path]
            return []

    # noinspection PyProtectedMember
    async def watch_component_modified(self, path: Path) -> list:
        """Hook that is called when a component file is modified"""

        routes = []
        if (self.path / 'components').resolve() in path.parents:
            for component in SlApp._components.copy():
                if str(component["source_path"].resolve()) == str(path.resolve()):
                    SlApp._components.remove(component)
                    SloDebugHandler.delete_json(base_key="registered_components", sub_key=component["uri"])
                    routes.append(component["uri"])
        return routes

    # noinspection PyProtectedMember
    # Todo:  components checking is redundant here
    async def watch_app_added(self, path: Path) -> list | list[str] | None:
        """Hook that is called when the app file is created"""

        routes = []
        if (self.path / "app.py").resolve() == path.resolve():
            for component in AppComponent._components:
                routes.append(component["uri"])


        return routes


    # noinspection PyProtectedMember
    async def watch_app_modified(self, path: Path) -> list:
        """Hook that is called when the app file is modified"""
        routes = []
        if (self.path / "app.py").resolve() == path.resolve():
            print("[1]" "-" * 20, AppComponent._components, "-"*20)
            for component in AppComponent._components.copy():
                AppComponent._components.remove(component)
                routes.append(component["uri"])
            print("[2]" "-" * 20, AppComponent._components, "-" * 20)
        return routes

    # noinspection PyProtectedMember
    async def watch_root(self, path):
        """Watch the root folder for changes"""
        console.print(f"[bold italic yellow]Watching {str(path.resolve())} for changes")
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
                            await callback["changes_done"](path)  # call the reload_all_css with parameter: path


                    await self.rpc.hot_reload_routes(routes)

    # noinspection PyMethodMayBeStatic
    async def on_start(self, port):
        """Hook that is called when the app starts"""
        self.watch_callbacks = [
            {
                "added": self.watch_component_added,
                "modified": self.watch_component_modified,
                "removed": self.watch_component_modified,
                "changes_done": None
            },
            {
                "added": self.watch_app_added,
                "modified": self.watch_app_modified,
                "removed": self.watch_app_modified,
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


class Name(Widget):
    selected_preprocessor_name = reactive("")

    def render(self):
        return f"Selected css library: {self.selected_preprocessor_name}" if self.selected_preprocessor_name != "" else ""


class GenerateOption(Static):
    text = reactive("")

    def __init__(self, text):
        super().__init__()
        self.original_text = text
        self.text = text
        self.input = ""

    def render(self):
        """Used to render the text"""
        return self.text

    def text_input(self, key: Key):
        if key.key == "backspace":
            self.input = self.input[:-1]
        else:
            self.input += key.char

        self.text = self.original_text + self.input


class BufferWidget(Static):
    buffer = reactive("")

    def render(self):
        self.styles.height = len(self.buffer.split("\n"))
        return self.buffer


class ComponentFromJson:

    # noinspection PyMethodMayBeStatic
    # noinspection PyProtectedMember
    @classmethod
    def get_registered_components(cls):
        return SloDebugHandler._load()["registered_components"]

    # noinspection PyMethodMayBeStatic
    # noinspection PyProtectedMember
    @classmethod
    def get_app_components(cls):
        return SloDebugHandler._load()["app_components"]


class Component(Static):
    def __init__(self, component):
        super().__init__()

        self.component = component

    def render(self):
        return self.component


class SloText(App):
    BINDINGS = [
        Binding(
            key="q", action="quit", description="Quit the app"),
    ]
    selected_preprocessor: int = 0
    selection = reactive([GenerateOption("") for _ in range(5)])
    # current_header = GenerateOption("Pick a UI framework preset:")
    current_header = GenerateOption("")
    buffer = BufferWidget()

    PREPROCESSOR_INFORMATION: dict[str, list] = {
        "tailwind": ["npm install tailwindcss", "npx tailwindcss -i ./css/input.css -o ./css/output.css --watch"],
        "bootstrap": ["npm install bootstrap", "npm run"],
        "sass": ["npm install node-sass --save", "npm run"]
    }

    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = {}
        self.stage = "projName"
        super().__init__()

    def compose(self) -> ComposeResult:
        """The body"""

        yield self.buffer
        yield self.current_header
        for x in self.selection:
            yield x
        yield Footer()

    def on_mount(self):
        """Hook that is called when the app is mounted"""
        # self.selection[ self.selected_preprocessor].text = f"[cyan]> {self.selection[
        # self.selected_preprocessor].original_text}[/cyan]"
        # White here is actually grey
        initial_text = f"[green]?[/green] Project Name [white]({self.path.name})[/white]: [cyan]"
        self.current_header.original_text, self.current_header.text = initial_text, initial_text

    def on_key(self, event: Key) -> None:
        """Handle key presses"""
        if self.stage == "projName":
            if event.key == "enter":
                self.stage = "version"
                if self.current_header.input == "":
                    self.current_header.input = self.path.name
                self.data["name"] = self.current_header.input
                self.buffer.buffer += f"[green]?[/green] Project name: [cyan]{self.data['name']}[/cyan]\n"
                self.current_header.input = ""
                self.current_header.original_text = f"[green]?[/green] Version [white](1.0.0)[/white]: [cyan]"
                self.current_header.text = f"[green]?[/green] Version [white](1.0.0)[/white]: [cyan]"
            else:
                self.current_header.text_input(event)
        elif self.stage == "version":
            if event.key == "enter":
                self.stage = "description"
                if self.current_header.input == "":
                    self.current_header.input = "1.0.0"
                self.data["version"] = self.current_header.input
                self.buffer.buffer += f"[green]?[/green] Version: [cyan]{self.data['version']}[/cyan]\n"
                self.current_header.input = ""
                self.current_header.original_text = f"[green]?[/green] Description [white](A Sloby project)[/white]: " \
                                                    f"[cyan] "
                self.current_header.text = f"[green]?[/green] Description [white](A Sloby project)[/white]: "
            else:
                self.current_header.text_input(event)
        elif self.stage == "description":
            if event.key == "enter":
                self.stage = "preprocessor"
                if self.current_header.input == "":
                    self.current_header.input = "A Sloby project"
                self.data["description"] = self.current_header.input
                self.buffer.buffer += f"[green]?[/green] Description: [cyan]{self.data['description']}[/cyan]\n"
                self.current_header.text = f"[green]?[/green] Author [white](None)[/white]: [cyan]"
                self.current_header.input = ""
                self.current_header.text = f"[green]?[/green] Pick a UI framework preset: "
                new_selection = ["None", "Tailwind", "Bootstrap", "Animate", "Sass"]
                for old, new in zip(self.selection, new_selection):
                    old.original_text = new
                    old.text = new
                self.selection[0].text = f"[cyan]> {self.selection[0].original_text}[/cyan]"
            else:
                self.current_header.text_input(event)
        elif self.stage == "preprocessor":
            if event.key in ("down", "up"):
                if event.key == "down":
                    previous_selected = self.selected_preprocessor
                    if self.selected_preprocessor == len(self.selection) - 1:
                        self.selected_preprocessor = -1
                    modifier = 1
                else:
                    previous_selected = self.selected_preprocessor
                    if self.selected_preprocessor == 0:
                        self.selected_preprocessor = len(self.selection)
                    modifier = -1
                current_text = self.selection[self.selected_preprocessor + modifier]
                current_text.text = f"[cyan]> {current_text.text}[/cyan]"
                previous_text = self.selection[previous_selected]
                previous_text.text = previous_text.original_text
                self.selected_preprocessor += modifier

            if event.key == "enter":
                self.buffer.buffer = f"[green]?[/green] UI Framework: [cyan]{self.selection[self.selected_preprocessor].original_text}[/cyan]\n"
                self.current_header.text = "Example header"

    def get_selected_preprocessor(self) -> list[str, str]:
        """Used to return the selected preprocessor"""
        selected_preprocessor_text = self.selection[self.selected_preprocessor].original_text.lower()
        return [selected_preprocessor_text, self.PREPROCESSOR_INFORMATION[selected_preprocessor_text][1]]


class SloInspector(App):
    BINDINGS = [
        Binding(
            key="q", action="quit", description="Quit the app"),
    ]
    buffer = BufferWidget()

    registered_component = []
    app_component = []

    def __init__(self):
        super().__init__()

    def compose(self):
        yield self.buffer
        # Registered components
        for component in ComponentFromJson.get_registered_components():
            yield Component(component)
        # App Components
        for component in ComponentFromJson.get_registered_components():
            yield Component(component)

        yield Footer()


def start_typer():
    """Start the typer app"""
    app()


if __name__ == "__main__":
    start_typer()
