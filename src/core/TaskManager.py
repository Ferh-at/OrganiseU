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
            # Subtasks table
            Cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS subtasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
                )
                """
            )
            # Indexes
            Cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_username ON tasks(username)"
            )
            Cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_subtasks_task_id ON subtasks(task_id)"
            )
            Conn.commit()

    def AddTask(self, Username, Title, Description=None, Subtasks=None):
        if not Username or not Title:
            raise ValueError("username and title are required")
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "INSERT INTO tasks (username, title, description) VALUES (?, ?, ?)",
                (Username, Title, Description),
            )
            TaskID = int(Cursor.lastrowid)

            # Add subtasks if provided
            if Subtasks:
                for SubtaskTitle in Subtasks:
                    if SubtaskTitle.strip():
                        Cursor.execute(
                            "INSERT INTO subtasks (task_id, title) VALUES (?, ?)",
                            (TaskID, SubtaskTitle.strip()),
                        )

            Conn.commit()
            return TaskID

    def GetTasks(self, Username):
        # * Return list of (id, title, status, description) for a user's tasks
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "SELECT id, title, status, description FROM tasks WHERE username = ? ORDER BY id DESC",
                (Username,),
            )
            Rows = Cursor.fetchall() or []
        return [
            (int(Row[0]), str(Row[1]), str(Row[2]), str(Row[3]) if Row[3] else None)
            for Row in Rows
        ]

    def GetSubtasks(self, TaskID):
        # * Return list of (id, title, status) for subtasks of a task
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "SELECT id, title, status FROM subtasks WHERE task_id = ? ORDER BY id ASC",
                (TaskID,),
            )
            Rows = Cursor.fetchall() or []
        return [(int(Row[0]), str(Row[1]), str(Row[2])) for Row in Rows]

    def GetTaskWithSubtasks(self, TaskID):
        # * Return task details with all its subtasks
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "SELECT id, title, description, status FROM tasks WHERE id = ?",
                (TaskID,),
            )
            TaskRow = Cursor.fetchone()
            if not TaskRow:
                return None

            Subtasks = self.GetSubtasks(TaskID)

            return {
                "id": TaskRow[0],
                "title": TaskRow[1],
                "description": TaskRow[2],
                "status": TaskRow[3],
                "subtasks": Subtasks,
            }

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

    def CompleteSubtask(self, SubtaskID):
        # * Mark subtask as complete and auto-complete parent if all subtasks done
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()

            # Get parent task ID
            Cursor.execute("SELECT task_id FROM subtasks WHERE id = ?", (SubtaskID,))
            Result = Cursor.fetchone()
            if not Result:
                return False

            TaskID = Result[0]

            Cursor.execute(
                "UPDATE subtasks SET status = 'completed' WHERE id = ?", (SubtaskID,)
            )

            Cursor.execute(
                "SELECT COUNT(*) FROM subtasks WHERE task_id = ? AND status = 'pending'",
                (TaskID,),
            )
            PendingCount = Cursor.fetchone()[0]

            if PendingCount == 0:
                Cursor.execute(
                    "UPDATE tasks SET status = 'completed' WHERE id = ?", (TaskID)
                )

            Conn.commit()
            return True

    def CompleteTask(self, TaskID):
        # * Mark task and all its subtasks as complete
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()

            Cursor.execute(
                "UPDATE tasks SET status = 'completed' WHERE id = ?", (TaskID,)
            )

            Cursor.execute(
                "UPDATE subtasks SET status = 'completed' WHERE task_id = ?", (TaskID,)
            )

            Conn.commit()
            return True

    def DeleteTask(self, TaskID):
        # * Delete task and all its subtasks
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()

            Cursor.execute("DELETE FROM subtasks WHERE task_id = ?", (TaskID,))

            Cursor.execute("DELETE FROM tasks WHERE id = ?", (TaskID,))

            Conn.commit()
            return True

    def AddSubtask(self, TaskID, SubtaskTitle):
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                "INSERT INTO subtasks (task_id, title) VALUES (?, ?)",
                (TaskID, SubtaskTitle),
            )
            Conn.commit()
            return int(Cursor.lastrowid)



