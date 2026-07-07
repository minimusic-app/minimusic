import os
import sys
import time
from rich.console import Console
from config.serverenv import PORT
import threading
import socket
import mimetypes

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from api.server import runServer

console = Console()

def mimetypes_start():

    console.log("[bold green] Starting Mimetypes... [/bold green]")
    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("text/javascript", ".js")
    mimetypes.add_type("text/html", ".html")
    mimetypes.add_type("image/png", ".png")
    mimetypes.add_type("image/webp", ".webp")

class Starter:
    def __init__(self, port: PORT) -> None:
        self.port = port or int(PORT)
        self.ip = f"http://127.0.0.1:{self.port}"

    
    def get_local_ip(self) -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def start_server_as_thread(self):
        thread = threading.Thread(target=runServer, daemon=True)
        thread.start()
        console.log("[bold green] Server started! [/bold green]")
        console.log("\n")
        console.log(f"[bold] Local: http://127.0.0.1:{self.port} [/bold]")
        console.log(f"[bold] Network: http://{self.get_local_ip()}:{self.port}")
        
    
def start_minimusic():
    # First, start mimetypes
    mimetypes_start()
    starter = Starter(port=int(PORT))
    starter.start_server_as_thread()
    

if __name__=="__main__":
    start_minimusic()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        console.log("[red] Closing Server... [/red]")
