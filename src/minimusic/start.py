import os
import sys
import time
from config.serverenv import PORT
from utils.logging import Logger, Colors
import threading
import socket
import mimetypes

logger = Logger()
color = Colors()

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from api.server import runServer


def mimetypes_start():

    logger.print("[bold green] Starting Mimetypes... [/bold green]")
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
        logger.print("Server started!")
        logger.print("\n")
        logger.print(f"Local: http://127.0.0.1:{self.port}")
        logger.print(f"Network: http://{self.get_local_ip()}:{self.port}")
        
    
def start_minimusic():
    from builder import build_minimusic

    if not getattr(sys, "frozen", False):
        build_minimusic()
    
    mimetypes_start()
    starter = Starter(port=int(PORT))
    starter.start_server_as_thread()
    

if __name__=="__main__":
    start_minimusic()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        logger.print("Closing Server...")
