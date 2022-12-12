# Built-in
import sys
import typer
import importlib.util

from pathlib import Path

# This project
from slobypy.app import SlApp
import slobypy.react.design as design
from slobypy._templates import *

# Rich
from rich import print
from rich.columns import Columns

app = typer.Typer()


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
    SlApp.run(block=True)  # Don't block as we need to run the dash

    dash = SloDash(SlApp.rpc)


class SloDash:
    def __init__(self, rpc):
        self.rpc = rpc


if __name__ == "__main__":
    app()
