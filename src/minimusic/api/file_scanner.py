from pathlib import Path
from mutagen import File as MutagenFile
import json

ALLOWED_EXTENSIONS = {".mp3", ".flac", ".wav", ".ogg", ".m4a", ".aac", ".opus", ".wma"}

def extract_metadata(path: Path) -> dict:
    try:
        audio = MutagenFile(path, easy=True)
    except Exception:
        audio = None
    
    title  = None
    artist = None
    album  = None
    track  = None
    duration = 0.0
 
    if audio is not None:
        tags = audio.tags or {}
        title  = (tags.get("title")  or [None])[0]
        artist = (tags.get("artist") or [None])[0]
        album  = (tags.get("album")  or [None])[0]
        tracknum = (tags.get("tracknumber") or [None])[0]
        if tracknum:
            try:
                track = int(str(tracknum).split("/")[0])
            except ValueError:
                track = None
        if audio.info is not None:
            duration = getattr(audio.info, "length", 0.0)
 
    return {
        "title":    title or path.stem,
        "artist":   artist or "Unknown Artist",
        "album":    album or "Unknown Album",
        "duration": round(duration, 2),
        "track_no": track,
    }

def scan_user_folders(user_id: int, folders: list[str]) -> dict:
    found_paths: set[str] = set()
    added = 0
    skipped = 0

    for folder in folders:
        root = Path(folder)
        if not root.exists():
            return {"message": "Root Path doesn't exists."}

        for file_path in root.rglob("*"):
            if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
                continue
            if not file_path.is_file():
                continue

        abs_path = str(file_path.resolve())
        found_paths.add(abs_path)
        skipped += 1

        meta = extract_metadata(file_path)
        if meta is None:
            continue
        
        if meta["title"] == "":
            meta["title"] = file_path.stem
        if meta["artist"] == "":
            meta["artist"] = "Unknown Artist"
        if meta["album"] == "":
            meta["album"] = "Unknown Album"

def get_music_path(user_id: int, path: Path, root: list[str]) -> dict:
    try:
        with open(path, "r") as f:
            existing = json.load(f)
    except Exception as e:
        existing = {}
    abs_path = str(path.resolve())
    existing[abs_path] = extract_metadata(path)
    with open(path, "w") as f:
        json.dump(existing, f, indent=2)
    return existing

