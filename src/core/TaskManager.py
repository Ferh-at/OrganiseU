from utils.AuthenticationWrapper import GetDBConnection


class TaskManager:
    def __init__(self, DBPath="src/core/UsersDatabase.db"):
        self.DBPath = DBPath
        self._InitialiseDB()

    def _InitialiseDB(self):
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT DEFAULT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            # index to speed up user lookups
            Cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_username ON tasks(username)"
            )
            Conn.commit()

    def AddTask(self, Username, Title, Description=None):
        if not Username or not Title:
            raise ValueError("username and title are required")
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "INSERT INTO tasks (username, title, description) VALUES (?, ?, ?)",
                (Username, Title, Description),
            )
            Conn.commit()
            return int(Cursor.lastrowid)

    def GetTasks(self, Username):
        # * Return list of (id, title) for a user's tasks ordered by newest first.
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "SELECT id, title FROM tasks WHERE username = ? ORDER BY id DESC",
                (Username,),
            )
            Rows = Cursor.fetchall() or []
        return [(int(Row[0]), str(Row[1])) for Row in Rows]

    def CountTasks(self, Username):
        # * Return (total, completed, pending) counts for a user.
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE username = ?",
                (Username,),
            )
            Total = int(Cursor.fetchone()[0] or 0)
            Cursor.execute(
                "SELECT COUNT(*) FROM tasks WHERE username = ? AND status = 'completed'",
                (Username,),
            )
            Completed = int(Cursor.fetchone()[0] or 0)
            Pending = max(0, Total - Completed)
        return Total, Completed, Pending
