import os
import sys
import time
from rich.console import Console

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from minimusic.api.server import runServer

console = Console()

def main():
    console.print("[bold green]Starting MiniMusic...[/bold green]")
    time.sleep(3)
    console.print("[bold yellow]Starting MiniMusic Server...[/bold yellow]")
    time.sleep(2)
    runServer()  # Start the server API


if __name__ == "__main__":
    main()
