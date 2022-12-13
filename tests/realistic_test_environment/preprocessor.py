import asyncio
import subprocess
import sys
from asyncio import AbstractEventLoop
from datetime import datetime
from pathlib import Path
from typing import Type

css_process = None
css_event = asyncio.Event()


def init() -> dict:
    global css_process

    # css_process = await asyncio.create_subprocess_shell(
    #     "npx tailwindcss -i ./css/input.css -o ./css/output.css --watch",
    #     stdout=asyncio.subprocess.PIPE,
    #     stderr=asyncio.subprocess.PIPE,
    # )

    css_process = subprocess.Popen(
        "npx tailwindcss -i ./css/input.css -o ./css/output.css --watch",
        stdout=subprocess.PIPE,
        shell=True
    )

    return {
        "process_css": process_css,
        "tasks": [_read_css_stream]
    }


def _read_css_stream():
    global css_event
    # while True:
    #     print("waiting")
    #     line = await stream.readline()
    #     print("got line")
    #     if line:
    #         if line.startswith(b"Rebuilding..."):
    #             css_event.clear()
    #         elif line.startswith(b"Done in"):
    #             css_event.set()
    #     else:
    #         break

    line = ''
    for data in iter(lambda: css_process.stderr.read(1), b""):
        line += data.decode('utf-8')

        if data.decode('utf-8') == '\n':
            if line.startswith("Rebuilding..."):
                css_event.clear()
            elif line.startswith("Done in"):
                css_event.set()
            line = ''


async def process_css() -> Path:
    global css_event
    await css_event.wait()
    return Path("css/output.css")
