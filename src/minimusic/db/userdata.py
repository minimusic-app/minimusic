import sqlite3 as sqlite
from werkzeug.security import generate_password_hash

conn = sqlite.connect("user.db")
cur = conn.cursor()

class UserData:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
                    username TEXT UNIQUE NOT NULL,
                    id INTEGER PRIMARY_KEY AUTOINCREMENT,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user', 'guest'))
                )
    """)
    
    @classmethod
    def insert_guest_user():
        user = {
            "username": "guest",
            "password": generate_password_hash("guest"),
            "roles": "guest"
        }

        sqlite.SQLITE_INSERT