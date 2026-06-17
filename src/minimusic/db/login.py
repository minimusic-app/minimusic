import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("login.db")
cur = conn.cursor()

def get_user_from_db(username):
    cur.execute("SELECT password, role FROM users WHERE username = ?", username)
    result = cur.fetchone()
    return result # Return the data for validate in endpoint

def register_user(username, password, role='user'):
    hash_password = generate_password_hash(password)

    cur.execute(
        "INSERT INTO users (username, hash_password, role) VALUES (?, ?, ?)",
        (username, hash_password, role)
    )
    
def user_exists() -> bool:
    """True if at least one account exists (used to decide login vs onboarding)."""
        
    count = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    return count > 0

conn.commit() # Save
