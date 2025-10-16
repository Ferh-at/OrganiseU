from typing import List, Tuple, Optional

from utils.AuthenticationWrapper import GetDBConnection


class TaskManager:
    def __init__(self, DBPath: str = "src/core/UsersDatabase.db"):
        self.DBPath = DBPath
        self._initialise_db()

    def _initialise_db(self) -> None:
        """Ensure the tasks table exists."""
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
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
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_username ON tasks(username)"
            )
            conn.commit()

    def add_task(
        self, username: str, title: str, description: Optional[str] = None
    ) -> int:
        """Create a new task for a user and return the task id."""
        if not username or not title:
            raise ValueError("username and title are required")
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (username, title, description) VALUES (?, ?, ?)",
                (username, title, description),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def get_tasks(self, username: str) -> List[Tuple[int, str]]:
        """Return list of (id, title) for a user's tasks ordered by newest first."""
        with GetDBConnection(self.DBPath) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, title FROM tasks WHERE username = ? ORDER BY id DESC",
                (username,),
            )
            rows = cursor.fetchall() or []
        return [(int(row[0]), str(row[1])) for row in rows]
