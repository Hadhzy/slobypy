from string import Template

MAIN_FILE = """\
from slobypy.react import *

css = SCSSClass(
    name="parent",
    register=True
).child(
    SCSSClass(
        name="child1",
        display="block"
    ))
    
"""

COMPONENT_FILE = """\
from slobypy import SlApp
from slobypy.react import *
from slobypy import *

@SlApp.component("/route1")
class MyComponent1(Component):
    @property
    def name(self):
        return "MyComponent1"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P("test", className="parent", onClick=self.on_click)
        yield MyComponent2(props={"important_data": "Woah, this is a prop!"})

    def mount(self):
        pass


@SlApp.component("/route2")
class MyComponent2(Component):
    @property
    def name(self):
        return "MyComponent2"

    def on_click(self):
        print(self.name, "has been clicked!")

    def body(self):
        yield P(self.props["important_data"], className="parent", onClick=self.on_click)

    def mount(self):
        pass

"""

CONFIG = Template(
    """\
{
  "name": "My Project",
  "version": "1.0.0",
  "description": "My Project",
  "main": "app.py",
  "components": "components/",
  "scss": "scss/",
  "runtime_tasks": [],
  "processed_css": "",
  $preprocessor
  "processed_js": ""
}
"""
)

PREPROCESSOR = Template(
    """
import asyncio
from pathlib import Path

css_process = None
css_event = asyncio.Event()


async def init(rpc, cwd) -> dict:
    global css_process

    await rpc.log("Starting CSS watcher...")
    await rpc.log("Installing $library ...")
    # ENSURE that tailwindcss is installed, or else it blocks the program
    await asyncio.create_subprocess_shell("npm install $library", stdout=asyncio.subprocess.PIPE,
                                          stderr=asyncio.subprocess.PIPE, cwd=cwd.resolve())
    await rpc.log("Installation complete!")

    css_process = await asyncio.create_subprocess_shell(
        "$library_start",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    return {
        "process_css": process_css,
        "tasks": [_read_css_stream(css_process.stderr)]
    }


async def _read_css_stream(stream):
    while True:
        line = await stream.readline()
        if line:
            if line.startswith(b"Rebuilding..."):
                css_event.clear()
            elif line.startswith(b"Done in"):
                css_event.set()
        else:
            break


async def process_css() -> Path:
    global css_event
    await css_event.wait()
    return Path("css/output.css")

"""
)

SLO_DEBUG_HANDLER = """
{
    "registered_components": {},
    "app_components": {}
}
"""
