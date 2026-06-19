import os
import sys
import time
from rich.console import Console
from config.serverenv import PORT
import urllib.request
import webview
import threading
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from api.server import runServer

console = Console()

SERVER_URL = f"http://localhost:{PORT}"

def main():
    console.print("[bold green]Starting MiniMusic...[/bold green]")
    time.sleep(3)
    console.print("[bold yellow]Starting MiniMusic Server...[/bold yellow]")
    time.sleep(2)
    console.print(f"http://127.0.0.1:{PORT}")
    console.print(f"http://localhost:{PORT}")  

    server_thread = threading.Thread(target=runServer, daemon=True)
    server_thread.start()

    _wait_for_server(SERVER_URL)

    webview.create_window(
        "Mini Music",
        SERVER_URL,
        width=1100,
        height=700,
        min_size=(900, 600),
    )
    console.print("Calling webview.start()...")
    webview.start()

def _wait_for_server(url: str, timeout: float = 10.0):
    """Polls /health until the server responds or timeout is reached."""
    deadline = time.time() + timeout
    last_error = None
 
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"{url}/health", timeout=1)
            return
        except (urllib.error.URLError, ConnectionError) as e:
            last_error = e
            time.sleep(0.2)
 
    raise RuntimeError(
        f"MiniMusic server did not respond at {url} within {timeout}s. "
        f"Last error: {last_error}"
    )

if __name__ == "__main__":
    main()
