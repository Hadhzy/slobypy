# Built-in
import sys
import typer
import importlib.util
import socket
import urllib.request
import urllib.error

from pathlib import Path

# This project
from slobypy.app import SlApp
import slobypy.react.design as design
from slobypy._templates import *

# Rich
from rich import print
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer()
console = Console()


# Todo: Add design, run the files !not working
@app.command()
def components(registered: bool = False):
    # Used to return the components
    if registered:
        print(design.Design.USED_CLASSES)
    else:
        print(design.Design.get_registered_classes())


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

    with open(path / "main.py", "w") as f:
        f.write(MAIN_FILE)

    with open((path / "components") / "example_component.py", "w") as f:
        f.write(COMPONENT_FILE)


@app.command()
def run(file: str):
    # Attempt to import the file using importlib
    path = Path(file)
    try:
        spec = importlib.util.spec_from_file_location(path.name, path.resolve())
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.name] = module
        spec.loader.exec_module(module)
    except AttributeError:
        typer.echo("File not found")
        return

    # Attempt to run the app
    dash = SloDash()

    # Pash dash hook so that RPC updates can trigger UI changes
    SlApp.run(block=True, hooks=[dash], console=console)  # Don't block as we need to run the dash


class SloDash:
    def __init__(self):
        console.print("[blue]SlobyPy CLI v[cyan]1.0.0[/cyan] SloDash v[cyan]1.0.0[/cyan][/]\n")

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


if __name__ == "__main__":
    app()
