""""
The tools that Mini Music provides without UI.
"""

from getpass import getpass
from db.userdata import UserData
from db.setup import setup_userdata_sqlite
from werkzeug.security import generate_password_hash as hash_password

def password_reset(password):
    setup_userdata_sqlite()

    try:
        print("Welcome to Mini Music Password Reset Handler!")
        username = input("enter your username:")
        user = UserData.get_by_username(username)

        if not user:
            print(f"User {username} not found.")
            return

        password = getpass("Enter password:")

    except KeyboardInterrupt:
        print("Cancelling operation...")
        return

    try:
        UserData.insert_user({"id": user.id, "password": hash_password(password)})
    except Exception as e:
        print(f"Error reseting password: {e}")

class anotherUserConfigs:
    showSinglesIcons: bool = True
    showFolders: bool = True
    