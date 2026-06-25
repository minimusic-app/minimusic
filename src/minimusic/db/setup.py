import sqlite3 as sqlite

conn_userdata = sqlite.connect("user.db")
conn_login = sqlite.connect("login.db")

def setup_userdata_sqlite():
    return conn_userdata

def setup_login_sqlite():
    return conn_login
