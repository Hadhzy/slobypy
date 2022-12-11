# Built-in
import sys
import typer
import importlib.util

from pathlib import Path
# This project
from slobypy.app import SlApp
import slobypy.react.design as design

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
    SlApp.run()  # Don't block as we need to run the dash

    dash = Slodash(SlApp.rpc)


class Slodash:
    def __init__(self, rpc):
        self.rpc = rpc


if __name__ == "__main__":
    app()
