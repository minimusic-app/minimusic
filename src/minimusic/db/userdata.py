import sqlite3 as sqlite
from werkzeug.security import generate_password_hash

conn = sqlite.connect("user.db")
cur = conn.cursor()


cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT UNIQUE NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user' CHECK(role IN ('admin', 'user', 'guest'))
    )
""")
conn.commit()

class UserData:
    @classmethod
    def insert_guest_user(cls):
        user = {
            "username": "guest",
            "password": generate_password_hash("guest"),
            "role": "guest"
        }

        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (user["username"], user["password"], user["role"])
        )
        conn.commit()
    
    @classmethod
    def insert_user(cls, username, password, role="user"):
       
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, generate_password_hash(password), role)
        )
        conn.commit()
    
    @classmethod
    def get_user_role(cls, username):
        
        cur.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        return result[0] if result else None
    
    @classmethod
    def is_guest(cls, username):
        
        return cls.get_user_role(username) == "guest"
    
    @classmethod
    def is_admin(cls, username):
        
        return cls.get_user_role(username) == "admin"

    @classmethod
    def get_by_username(cls, username: str):
        res = cur.execute("SELECT" + cls, "WHERE" + cls.id == id)

        return res
