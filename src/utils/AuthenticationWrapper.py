import sqlite3
from contextlib import contextmanager

@contextmanager
def GetDBConnection(DBPath="src/core/UsersDatabase.db"): #* if DBPath is not passed, it will default to the UsersDatabase.db
    conn = sqlite3.connect(DBPath)
    try:
        yield conn
    finally:
        conn.close()
