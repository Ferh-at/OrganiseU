import sqlite3
from contextlib import contextmanager

@contextmanager
def GetDBConnection(DBPath="data/users.db"):
    conn = sqlite3.connect(DBPath)
    try:
        yield conn
    finally:
        conn.close()
