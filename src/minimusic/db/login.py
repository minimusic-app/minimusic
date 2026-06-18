import sqlite3
from dataclasses import dataclass
from pathlib import Path
 
from werkzeug.security import generate_password_hash
 
DB_PATH = Path(__file__).resolve().parent / "login.db"
 
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        username      TEXT UNIQUE NOT NULL,
        hash_password TEXT NOT NULL,
        role          TEXT NOT NULL DEFAULT 'user'
    )
""")
conn.commit()
 
 
@dataclass
class User:
    id: int
    username: str
    password: str   
    role: str
 
 
def get_user_from_db(username: str) -> User | None:
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, hash_password, role FROM users WHERE username = ?",
        (username,),
    )
    row = cur.fetchone()
    if row is None:
        return None
    return User(id=row[0], username=row[1], password=row[2], role=row[3])
 
 
def register_user(username: str, password: str, role: str = "user") -> User | None:
    """
    Hashes `password` and inserts a new user.
    Returns the created User, or None if the username is already taken.
    """
    hashed = generate_password_hash(password)
    cur = conn.cursor()
 
    try:
        cur.execute(
            "INSERT INTO users (username, hash_password, role) VALUES (?, ?, ?)",
            (username, hashed, role),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return None
 
    return User(id=cur.lastrowid, username=username, password=hashed, role=role)
 
 
def user_exists() -> bool:
    """True if at least one account exists (used to decide login vs onboarding)."""
    cur = conn.cursor()
    count = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    return count > 0
