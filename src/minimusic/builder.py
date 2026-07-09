from rich.console import Console
from pathlib import Path
import subprocess
import sys
import os

console = Console()

def build_minimusic():
    if getattr(sys, "frozen", False):
        console.log(
            "[bold red] Build cannot run from the compiled executable. "
            "Run it from source instead, e.g. 'python -m minimusic.start' "
            "from the project root. [/bold red]"
        )
        return


    console.log("[bold yellow] Starting MiniMusic build... [/bold yellow]")

    main = "src/minimusic/start.py"

    actual_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    root_dir = (actual_dir / ".." / "..").resolve()
    script_path = root_dir / "src" / "minimusic" / "start.py"

    app_name = "minimusic-app"
    
    command = [
        "pyinstaller",
        "--onefile",
        f"--name={app_name}",
        f"--paths={actual_dir}",
        f"--paths={root_dir}",
        "--hidden-import=config",
        "--hidden-import=config.serverenv",
        "--hidden-import=api",
        "--hidden-import=api.server",
        str(script_path),
        main
    ]


    try:
        subprocess.run(command, check=True)
        console.log("[green] Build completed successfully! [/green]")
    except subprocess.CalledProcessError as e:
        console.log(f"[bold red] Failed to build MiniMusic: {e}")
