import datetime
from utils.AuthenticationWrapper import GetDBConnection


class HabitManager:
    def __init__(self, DBPath="src/core/UsersDatabase.db"):
        self.DBPath = DBPath
        self._InitialiseDB()

    def _InitialiseDB(self):
        """Initialize the habits and habit_tracking tables"""
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()

            # Habits table - stores habit definitions
            Cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    habit_name TEXT NOT NULL,
                    is_positive INTEGER DEFAULT 1,
                    goal_type TEXT DEFAULT 'increase',
                    baseline_count INTEGER DEFAULT 0,
                    target_count INTEGER DEFAULT 0,
                    target_date TEXT NOT NULL
                )
            """)

            # Habit tracking table - stores daily counts and targets
            Cursor.execute("""
                CREATE TABLE IF NOT EXISTS habit_tracking (
                    habit_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    count INTEGER DEFAULT 0,
                    suggested_target INTEGER DEFAULT 0,
                    PRIMARY KEY (habit_id, date),
                    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
                )
            """)

            # Index for faster queries
            Cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_habits_username 
                ON habits(username)
            """)

            Cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tracking_date 
                ON habit_tracking(date)
            """)

            Conn.commit()

    def AddHabit(
        self,
        username,
        habit_name,
        is_positive,
        goal_type,
        baseline_count,
        target_count,
        target_date,
    ):
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """
                INSERT INTO habits (username, habit_name, is_positive, goal_type, baseline_count, target_count, target_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    username,
                    habit_name,
                    is_positive,
                    goal_type,
                    baseline_count,
                    target_count,
                    target_date,
                ),
            )
            habit_id = Cursor.lastrowid

            today = datetime.date.today().isoformat()
            Cursor.execute(
                """
                INSERT INTO habit_tracking (habit_id, date, count, suggested_target)
                VALUES (?, ?, 0, ?)
            """,
                (habit_id, today, baseline_count),
            )

            Conn.commit()
            return habit_id

    def GetUserHabits(self, username):
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """
                SELECT id, habit_name, is_positive, goal_type, 
                       baseline_count, target_count, target_date
                FROM habits
                WHERE username = ?
            """,
                (username,),
            )

            habits = []
            for row in Cursor.fetchall():
                habits.append(
                    {
                        "id": row[0],
                        "habit_name": row[1],
                        "is_positive": row[2],
                        "goal_type": row[3],
                        "baseline_count": row[4],
                        "target_count": row[5],
                        "target_date": row[6],
                    }
                )
            return habits

    def GetTodayData(self, habit_id):
        """Get today's count and suggested target for a habit"""
        today = datetime.date.today().isoformat()

        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """
                SELECT count, suggested_target
                FROM habit_tracking
                WHERE habit_id = ? AND date = ?
            """,
                (habit_id, today),
            )

            row = Cursor.fetchone()
            if row:
                return {"count": row[0], "suggested_target": row[1]}
            return None

    def IncrementHabit(self, habit_id):
        today = datetime.date.today().isoformat()

        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()

            Cursor.execute(
                """
                SELECT count FROM habit_tracking
                WHERE habit_id = ? AND date = ?
            """,
                (habit_id, today),
            )

            row = Cursor.fetchone()
            if row:
                Cursor.execute(
                    """
                    UPDATE habit_tracking
                    SET count = count + 1
                    WHERE habit_id = ? AND date = ?
                """,
                    (habit_id, today),
                )
            else:
                # safety measure in case the row doesn't exist
                Cursor.execute(
                    """
                    INSERT INTO habit_tracking (habit_id, date, count, suggested_target)
                    VALUES (?, ?, 1, 0)
                """,
                    (habit_id, today),
                )

            Conn.commit()

    def DeleteHabit(self, habit_id):
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            Conn.commit()

    def _GetUserStats(self, username):
        """Fetch user stats (discipline, motivation, concentration, energy) from users table"""
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """
                SELECT concentration, discipline, motivation, energy
                FROM users
                WHERE username = ? 
                """,(username,),
            )

            row = Cursor.fetchone()
            if row:
                return {
                    "concentration": row[0],
                    "discipline": row[1],
                    "motivation": row[2],
                    "energy": row[3],
                }
            return {"concentration": 5, "discipline": 5, "motivation": 5, "energy": 5}

    def CalculatePreview(self, baseline, target, target_date, discipline):
        try:
            if isinstance(target_date, str):
                target_date_obj = datetime.datetime.strptime(
                    target_date, "%Y-%m-%d"
                ).date()
            else:
                target_date_obj = target_date

            today = datetime.date.today()
            days = (target_date_obj - today).days

            if days <= 0:
                return "Target date must be in the future"

            total_change = abs(target - baseline)
            avg_daily = total_change / days

            # Adjust for discipline
            if discipline <= 3:
                adjusted = avg_daily * 0.8
            elif discipline >= 8:
                adjusted = avg_daily * 1.2
            else:
                adjusted = avg_daily

            # Warning for unrealistic goals
            if adjusted > 5:
                return f"⚠️ ~{adjusted:.1f} per day (Very challenging!)"
            elif adjusted > 3:
                return f"⚠️ ~{adjusted:.1f} per day (Challenging)"
            else:
                return f"~{adjusted:.1f} per day on average"

        except Exception as e:
            return f"Error: {str(e)}"

    def CheckAndGenerateDailyGoals(self, username):
        today = datetime.date.today().isoformat()
        habits = self.GetUserHabits(username)
        stats = self._GetUserStats(username)
        discipline = stats["discipline"]

        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()

            for habit in habits:
                habit_id = habit["id"]
                Cursor.execute(
                    """
                    SELECT count, suggested_target FROM habit_tracking
                    WHERE habit_id = ? AND date = ?
                """,
                    (habit_id, today),
                )

                row = Cursor.fetchone()
                if row is not None:
                    # Entry exists, skip
                    continue

                new_target = self._CalculateNewTarget(habit, discipline, Cursor)

                Cursor.execute(
                    """
                    INSERT INTO habit_tracking (habit_id, date, count, suggested_target)
                    VALUES (?, ?, 0, ?)
                """,
                    (habit_id, today, new_target),
                )

            Conn.commit()

    def _CalculateNewTarget(self, habit, discipline, cursor):
        today = datetime.date.today()
        habit_id = habit["id"]
        goal_type = habit["goal_type"]
        target_count = habit["target_count"]
        target_date = datetime.datetime.strptime(
            habit["target_date"], "%Y-%m-%d"
        ).date()

        # retrieving yesterday's data
        yesterday = (today - datetime.timedelta(days=1)).isoformat()
        cursor.execute(
            """
            SELECT count, suggested_target FROM habit_tracking
            WHERE habit_id = ? AND date = ?
        """,
            (habit_id, yesterday),
        )

        yesterday_row = cursor.fetchone()

        if yesterday_row:
            yesterday_count = yesterday_row[0]
            current_target = yesterday_row[1]
        else:
            # First day, use baseline
            current_target = habit["baseline_count"]
            yesterday_count = None

        # 1. Calculate time-based pace
        days_remaining = (target_date - today).days

        if days_remaining <= 0:
            # Target date reached, maintain target
            return target_count

        if goal_type == "decrease":
            points_remaining = current_target - target_count
        else:  # increase
            points_remaining = target_count - current_target

        base_daily_change = points_remaining / (
            days_remaining if days_remaining > 0 else 0
        )

        # 2. Check user performance
        performance_multiplier = 1.0
        if yesterday_count is not None and yesterday_row[1] > 0:
            yesterday_target = yesterday_row[1]

            if goal_type == "decrease":
                if yesterday_count <= yesterday_target * 0.8:
                    performance_multiplier = 1.4
                elif yesterday_count <= yesterday_target:
                    performance_multiplier = 1.0
                else:
                    performance_multiplier = 0.75
            else:
                if yesterday_count >= yesterday_target * 1.2:
                    performance_multiplier = 1.4
                elif yesterday_count >= yesterday_target:
                    performance_multiplier = 1.0
                else:
                    performance_multiplier = 0.75

        # 3. Factor in discipline
        discipline_factor = 1.0
        if discipline >= 8:
            discipline_factor = 1.2
        elif discipline <= 3:
            discipline_factor = 0.8

        # 4. Calculate adaptive change
        daily_change = base_daily_change * performance_multiplier * discipline_factor

        if goal_type == "decrease":
            new_target = current_target - daily_change
            new_target = max(new_target, target_count)
        else:
            new_target = current_target + daily_change
            new_target = min(new_target, target_count)

        return int(round(new_target))