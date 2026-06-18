import os
import sys
import time
from rich.console import Console

# FIX: Imported 'PORT' from config.serverenv to prevent a NameError.
# This ensures the print statement below can successfully display the port number.
from config.serverenv import PORT

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
    print(f"Server running on http://localhost:{PORT}")
    runServer()  # Start the server API

if __name__ == "__main__":
    main()
