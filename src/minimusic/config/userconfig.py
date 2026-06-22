from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional
import json


@dataclass
class Config:
    finished: bool = field(default=False, init=True)
    cfgPathName: str = "userconfig.json"
    cfgPath: Path = Path('.')
    userId: int = 0

    serverId: str = ""
    usersConnected: bool = True

    showAlbumsAsSingles: bool = False
    cleanAlbumTitle: bool = True

    showPlaylistsAsFolder: bool = False

    def load_config(self) -> Optional[Any]:
        """Load the user config from the file named by `cfgPathName`.

        Returns the parsed JSON object, or None if the file doesn't exist.
        """
        file_path = self.cfgPath / self.cfgPathName
        if not file_path.exists():
            return None
        return json.loads(file_path.read_text(encoding="utf-8"))

    def write_file(self, data: Any) -> Path:
        """Write `data` as JSON to the config file named by `cfgPathName`.

        Ensures the directory exists and returns the written file path.
        """
        file_path = self.cfgPath / self.cfgPathName
        self.cfgPath.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return file_path
