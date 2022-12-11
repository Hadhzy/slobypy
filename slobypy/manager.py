# Built-in
import sys
import typer
import importlib.util

from pathlib import Path
# This project
from slobypy.app import SlApp
import slobypy.react.design as design

app = typer.Typer()


#Todo: Add design, run the files !not working
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
    user_app = SlApp.instance
    user_app.run()



if __name__ == "__main__":
    app()
