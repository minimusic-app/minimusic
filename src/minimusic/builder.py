from rich.console import Console
import subprocess
import sys
import os

console = Console()

def build_minimusic():
    console.log("[bold yellow] Starting MiniMusic build... [/bold yellow]")

    main = "src/minimusic/start.py"

    app_name = "minimusic-app"
    
    command = [
        "pyinstaller",
        "--onefile",
        f"--name={app_name}"
    ]

    command.append(main)

    try:
        subprocess.run(command, check=True)
        console.log("[green] Build completed successfully! [/green]")
    except subprocess.CalledProcessError as e:
        console.log(f"[bold red] Failed to build MiniMusic: {e}")
