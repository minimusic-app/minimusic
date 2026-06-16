from dotenv import load_dotenv
from pathlib import Path
from os import getenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / "server.env")

raw_port = getenv("SERVER_PORT")
try:
    PORT = int(raw_port) if raw_port is not None else 8000
except ValueError:
    PORT = 8000