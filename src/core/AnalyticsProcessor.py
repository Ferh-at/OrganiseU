import datetime
from typing import Any
from core.TaskManager import TaskManager
from core.HabitManager import HabitManager
from utils.AuthenticationWrapper import GetDBConnection


class AnalyticsProcessor:
    def __init__(self, DBPath="src/core/UsersDatabase.db"):
        self.DBPath = DBPath
        self.TaskManager = TaskManager(DBPath)
        self.HabitManager = HabitManager(DBPath)

    def _get_date_range(self, time_range):
        today = datetime.date.today()
        
        if time_range == "today":
            start_date = today
            end_date = today
        elif time_range == "this_week":
            # Get Monday of current week
            days_since_monday = today.weekday()
            start_date = today - datetime.timedelta(days=days_since_monday)
            end_date = today
        elif time_range == "this_month":
            start_date = today.replace(day=1)
            end_date = today
        elif time_range == "all_time":
            start_date = None
            end_date = None
        else:
            start_date = today
            end_date = today
        
        return start_date, end_date

    def _parse_date(self, date_str):
        if isinstance(date_str, datetime.date):
            return date_str
        try:
            return datetime.datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        except:
            try:
                return datetime.datetime.fromisoformat(date_str).date()
            except:
                return None

    def _filter_by_date_range(self, date_str, start_date, end_date):
        if start_date is None or end_date is None:
            return True
        date_obj = self._parse_date(date_str)
        if date_obj is None:
            return False
        return start_date <= date_obj <= end_date


    def get_task_stats(self, username, time_range="all_time"): # defaults to all time if no time range is provided
        start_date, end_date = self._get_date_range(time_range)
        
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            
            if start_date is None: # MEANS IT'S ALL TIME
                Cursor.execute(
                    "SELECT COUNT(*) FROM tasks WHERE username = ?",
                    (username,)
                )
                total = Cursor.fetchone()[0]
                
                Cursor.execute(
                    "SELECT COUNT(*) FROM tasks WHERE username = ? AND status = 'completed'",
                    (username,)
                )
                completed = Cursor.fetchone()[0]
            else:
                start_str = start_date.isoformat()
                end_str = end_date.isoformat()
                
                Cursor.execute(
                    """SELECT COUNT(*) FROM tasks 
                    WHERE username = ? AND created_at >= ? AND created_at <= ?""",
                    (username, start_str, end_str + " 23:59:59")
                )
                total = Cursor.fetchone()[0]
                
                Cursor.execute(
                    """SELECT COUNT(*) FROM tasks 
                    WHERE username = ? AND status = 'completed' 
                    AND created_at >= ? AND created_at <= ?""",
                    (username, start_str, end_str + " 23:59:59")
                )
                completed = Cursor.fetchone()[0]
            
            pending = max(0, total - completed)
            completion_rate = (completed / total * 100) if total > 0 else 0 #precaution to default completion rate to 0 if no tasks are found
            
            return {
                "total": total,
                "completed": completed,
                "pending": pending,
                "completion_rate": round(completion_rate, 1)
            }

    def get_task_trends(self, username, time_range="all_time"):
        start_date, end_date = self._get_date_range(time_range)
        
        if start_date is None:
            # Get earliest task date
            with GetDBConnection(self.DBPath) as Conn:
                Cursor = Conn.cursor()
                Cursor.execute(
                    """SELECT MIN(created_at) FROM tasks WHERE username = ?""",
                    (username,)
                )
                result = Cursor.fetchone()[0]
                if result:
                    start_date = self._parse_date(result)
                    if start_date is None:
                        start_date = datetime.date.today()
                else:
                    start_date = datetime.date.today()
                end_date = datetime.date.today()
        
        # Get all tasks in range
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            start_str = start_date.isoformat()
            end_str = end_date.isoformat()
            
            # Get all tasks in range
            Cursor.execute(
                """SELECT created_at, status
                FROM tasks 
                WHERE username = ? AND created_at >= ? AND created_at <= ?""",
                (username, start_str, end_str + " 23:59:59")
            )
            all_rows = Cursor.fetchall()
        
        # Organize data by date
        daily_data = {}
        current_date = start_date
        while current_date <= end_date:
            daily_data[current_date.isoformat()] = {"created": 0, "completed": 0}
            current_date += datetime.timedelta(days=1)
        
        # Process rows and group by date
        for row in all_rows:
            created_at_str, status = row
            date_obj = self._parse_date(created_at_str)
            if date_obj and date_obj.isoformat() in daily_data:
                date_iso = date_obj.isoformat()
                daily_data[date_iso]["created"] += 1
                if status == "completed":
                    daily_data[date_iso]["completed"] += 1
        
        # Calculate completion rates
        dates = sorted(daily_data.keys())
        completion_rates = []
        cumulative_completed = 0
        cumulative_total = 0
        
        for date_str in dates:
            data = daily_data[date_str]
            cumulative_total += data["created"]
            cumulative_completed += data["completed"]
            if cumulative_total > 0:
                rate = (cumulative_completed / cumulative_total) * 100
            else:
                rate = 0
            completion_rates.append(rate)
        
        return {
            "dates": dates,
            "completion_rates": completion_rates,
            "daily_completed": [daily_data[d]["completed"] for d in dates],
            "daily_created": [daily_data[d]["created"] for d in dates]
        }

    def get_task_comparison(self, username):
        """Returns week-over-week and month-over-month comparisons"""
        today = datetime.date.today()
        
        # This week
        days_since_monday = today.weekday()
        this_week_start = today - datetime.timedelta(days=days_since_monday)
        this_week_stats = self.get_task_stats(username, "this_week")
        
        # Last week
        last_week_end = this_week_start - datetime.timedelta(days=1)
        last_week_start = last_week_end - datetime.timedelta(days=6)
        
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """SELECT COUNT(*) FROM tasks 
                WHERE username = ? AND created_at >= ? AND created_at <= ?""",
                (username, last_week_start.isoformat(), last_week_end.isoformat() + " 23:59:59")
            )
            last_week_total = Cursor.fetchone()[0] or 0
            
            Cursor.execute(
                """SELECT COUNT(*) FROM tasks 
                WHERE username = ? AND status = 'completed' 
                AND created_at >= ? AND created_at <= ?""",
                (username, last_week_start.isoformat(), last_week_end.isoformat() + " 23:59:59")
            )
            last_week_completed = Cursor.fetchone()[0] or 0
        
        last_week_rate = (last_week_completed / last_week_total * 100) if last_week_total > 0 else 0
        
        # This month
        this_month_start = today.replace(day=1)
        this_month_stats = self.get_task_stats(username, "this_month")
        
        # Last month
        if today.month == 1:
            last_month_start = datetime.date(today.year - 1, 12, 1)
        else:
            last_month_start = datetime.date(today.year, today.month - 1, 1)
        
        if today.month == 1:
            last_month_end = datetime.date(today.year - 1, 12, 31)
        else:
            if today.month == 3:  # March
                last_month_end = datetime.date(today.year, 2, 28)
            elif today.month in [5, 7, 10, 12]:  # Months with 31 days before
                last_month_end = datetime.date(today.year, today.month - 1, 30)
            else:
                last_month_end = datetime.date(today.year, today.month - 1, 31)
        
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """SELECT COUNT(*) FROM tasks 
                WHERE username = ? AND created_at >= ? AND created_at <= ?""",
                (username, last_month_start.isoformat(), last_month_end.isoformat() + " 23:59:59")
            )
            last_month_total = Cursor.fetchone()[0] or 0
            
            Cursor.execute(
                """SELECT COUNT(*) FROM tasks 
                WHERE username = ? AND status = 'completed' 
                AND created_at >= ? AND created_at <= ?""",
                (username, last_month_start.isoformat(), last_month_end.isoformat() + " 23:59:59")
            )
            last_month_completed = Cursor.fetchone()[0] or 0
        
        last_month_rate = (last_month_completed / last_month_total * 100) if last_month_total > 0 else 0
        
        return {
            "week_over_week": {
                "this_week": this_week_stats["completion_rate"],
                "last_week": round(last_week_rate, 1),
                "change": round(this_week_stats["completion_rate"] - last_week_rate, 1)
            },
            "month_over_month": {
                "this_month": this_month_stats["completion_rate"],
                "last_month": round(last_month_rate, 1),
                "change": round(this_month_stats["completion_rate"] - last_month_rate, 1)
            }
        }

    def get_task_forecast(self, username):
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            Cursor.execute(
                """SELECT COUNT(*) FROM tasks 
                WHERE username = ? AND status = 'pending'""",
                (username,)
            )
            pending_count = Cursor.fetchone()[0] or 0
            
            Cursor.execute(
                """SELECT COUNT(*) FROM tasks 
                WHERE username = ? AND status = 'completed' 
                AND created_at >= ?""",
                (username, week_ago.isoformat())
            )
            completed_last_week = Cursor.fetchone()[0] or 0
        
        if completed_last_week > 0 and pending_count > 0:
            daily_rate = completed_last_week / 7.0
            days_to_complete = pending_count / daily_rate if daily_rate > 0 else 0
            forecast_date = today + datetime.timedelta(days=int(days_to_complete))
            return {
                "pending_tasks": pending_count,
                "daily_completion_rate": round(daily_rate, 1),
                "estimated_completion_date": forecast_date.isoformat(),
                "days_remaining": int(days_to_complete)
            }
        else:
            return {
                "pending_tasks": pending_count,
                "daily_completion_rate": 0,
                "estimated_completion_date": None,
                "days_remaining": None
            }

    def get_habit_stats(self, username, time_range="all_time"):
        start_date, end_date = self._get_date_range(time_range)
        habits = self.HabitManager.GetUserHabits(username)
        if not habits:
            return {
                "active_habits": 0,
                "total_habits": 0,
                "avg_completion_rate": 0,
                "habits_with_streaks": 0}

        total_habits = len(habits)
        completion_rates = []
        streaks_count = 0
        
        for habit in habits:
            habit_id = habit["id"]
            streaks = self.get_habit_streaks(username)
            if habit_id in streaks and streaks[habit_id]["current_streak"] > 0:
                streaks_count += 1
            
            if start_date is None: # all time
                with GetDBConnection(self.DBPath) as Conn:
                    Cursor = Conn.cursor()
                    Cursor.execute(
                        """SELECT COUNT(*), SUM(CASE WHEN count >= suggested_target THEN 1 ELSE 0 END)
                        FROM habit_tracking WHERE habit_id = ?""",
                        (habit_id,)
                    )
                    row = Cursor.fetchone()
                    if row and row[0] and row[0] > 0:
                        rate = (row[1] or 0) / row[0] * 100
                        completion_rates.append(rate)
            else:
                start_str = start_date.isoformat()
                end_str = end_date.isoformat()
                with GetDBConnection(self.DBPath) as Conn:
                    Cursor = Conn.cursor()
                    Cursor.execute(
                        """SELECT COUNT(*), SUM(CASE WHEN count >= suggested_target THEN 1 ELSE 0 END)
                        FROM habit_tracking 
                        WHERE habit_id = ? AND date >= ? AND date <= ?""",
                        (habit_id, start_str, end_str)
                    )
                    row = Cursor.fetchone()
                    if row and row[0] and row[0] > 0:
                        rate = (row[1] or 0) / row[0] * 100
                        completion_rates.append(rate)
        
        avg_completion_rate = sum(completion_rates) / len(completion_rates) if completion_rates else 0
        
        return {
            "active_habits": total_habits,
            "total_habits": total_habits,
            "avg_completion_rate": round(avg_completion_rate, 1),
            "habits_with_streaks": streaks_count
        }

    def get_habit_trends(self, username, time_range="all_time"):
        start_date, end_date = self._get_date_range(time_range)
        habits = self.HabitManager.GetUserHabits(username)
        
        if start_date is None:
            with GetDBConnection(self.DBPath) as Conn:
                Cursor = Conn.cursor()
                Cursor.execute("""SELECT MIN(date) FROM habit_tracking""")
                result = Cursor.fetchone()[0]
                if result:
                    start_date = self._parse_date(result)
                    if start_date is None:
                        start_date = datetime.date.today()
                else:
                    start_date = datetime.date.today()
                end_date = datetime.date.today()
        
        # Get tracking data
        habit_ids = [h["id"] for h in habits]
        if not habit_ids:
            return {"dates": [], "completion_percentages": [], "habit_data": {}}
        
        with GetDBConnection(self.DBPath) as Conn:
            Cursor = Conn.cursor()
            placeholders = ",".join("?" * len(habit_ids))
            start_str = start_date.isoformat()
            end_str = end_date.isoformat()
            
            Cursor.execute(
                f"""SELECT habit_id, date, count, suggested_target
                FROM habit_tracking
                WHERE habit_id IN ({placeholders}) AND date >= ? AND date <= ?
                ORDER BY date""",
                (*habit_ids, start_str, end_str)
            )
            rows = Cursor.fetchall()
        
        daily_data = {}
        current_date = start_date
        while current_date <= end_date:
            daily_data[current_date.isoformat()] = {"completed": 0, "total": 0}
            current_date += datetime.timedelta(days=1)
        
        habit_data = {hid: {"dates": [], "completion_rates": []} for hid in habit_ids}
        
        for row in rows:
            habit_id, date_str, count, target = row
            date_obj = self._parse_date(date_str)
            if date_obj and date_obj.isoformat() in daily_data:
                date_iso = date_obj.isoformat()
                daily_data[date_iso]["total"] += 1
                if target > 0 and count >= target:
                    daily_data[date_iso]["completed"] += 1
                
                # Per-habit data
                if habit_id in habit_data:
                    if date_iso not in habit_data[habit_id]["dates"]:
                        habit_data[habit_id]["dates"].append(date_iso)
                        rate = (count / target * 100) if target > 0 else 0
                        habit_data[habit_id]["completion_rates"].append(min(rate, 100))
        
        # Calculate overall completion percentages
        dates = sorted(daily_data.keys())
        completion_percentages = []
        for date_str in dates:
            data = daily_data[date_str]
            if data["total"] > 0:
                rate = (data["completed"] / data["total"]) * 100
            else:
                rate = 0
            completion_percentages.append(rate)
        
        return {
            "dates": dates,
            "completion_percentages": completion_percentages,
            "habit_data": habit_data
        }

    def get_habit_streaks(self, username):
        habits = self.HabitManager.GetUserHabits(username)
        streaks_data = {}
        
        for habit in habits:
            habit_id = habit["id"]
            target_count = habit["target_count"]
            goal_type = habit["goal_type"]
            
            with GetDBConnection(self.DBPath) as Conn:
                Cursor = Conn.cursor()
                Cursor.execute(
                    """SELECT date, count, suggested_target
                    FROM habit_tracking
                    WHERE habit_id = ?
                    ORDER BY date DESC""",
                    (habit_id,)
                )
                rows = Cursor.fetchall()
            
            if not rows:
                streaks_data[habit_id] = {
                    "habit_name": habit["habit_name"],
                    "current_streak": 0,
                    "longest_streak": 0
                }
                continue
            
            current_streak = 0
            longest_streak = 0
            temp_streak = 0
            
            # Process from most recent backwards (today first)
            today = datetime.date.today()
            
            # Sort rows by date descending
            sorted_rows = sorted(rows, key=lambda x: self._parse_date(x[0]) or datetime.date.min, reverse=True)
            
            for row in sorted_rows:
                date_str, count, suggested_target = row
                date_obj = self._parse_date(date_str)
                if date_obj is None or date_obj > today:
                    continue
                
                # Check if goal was met
                goal_met = False
                target_to_check = suggested_target if suggested_target > 0 else target_count
                if goal_type == "increase":
                    goal_met = count >= target_to_check
                else:  # decrease
                    goal_met = count <= target_to_check
                
                if goal_met:
                    current_streak += 1
                else:
                    # Streak broken
                    break
            
            # Calculate longest streak (process all dates)
            sorted_rows_asc = sorted(rows, key=lambda x: self._parse_date(x[0]) or datetime.date.min)
            temp_streak = 0
            for row in sorted_rows_asc:
                date_str, count, suggested_target = row
                date_obj = self._parse_date(date_str)
                if date_obj is None or date_obj > today:
                    continue
                
                target_to_check = suggested_target if suggested_target > 0 else target_count
                if goal_type == "increase":
                    goal_met = count >= target_to_check
                else:  # decrease
                    goal_met = count <= target_to_check
                
                if goal_met:
                    temp_streak += 1
                    longest_streak = max(longest_streak, temp_streak)
                else:
                    temp_streak = 0
            
            streaks_data[habit_id] = {
                "habit_name": habit["habit_name"],
                "current_streak": current_streak,
                "longest_streak": longest_streak
            }
        
        return streaks_data

    def get_habit_comparison(self, username):
        this_week_stats = self.get_habit_stats(username, "this_week")
        
        today = datetime.date.today()
        days_since_monday = today.weekday()
        this_week_start = today - datetime.timedelta(days=days_since_monday)
        last_week_end = this_week_start - datetime.timedelta(days=1)
        last_week_start = last_week_end - datetime.timedelta(days=6)
        
        habits = self.HabitManager.GetUserHabits(username)
        last_week_rates = []
        
        for habit in habits:
            habit_id = habit["id"]
            with GetDBConnection(self.DBPath) as Conn:
                Cursor = Conn.cursor()
                Cursor.execute(
                    """SELECT COUNT(*), SUM(CASE WHEN count >= suggested_target THEN 1 ELSE 0 END)
                    FROM habit_tracking
                    WHERE habit_id = ? AND date >= ? AND date <= ?""",
                    (habit_id, last_week_start.isoformat(), last_week_end.isoformat())
                )
                row = Cursor.fetchone()
                if row and row[0] and row[0] > 0:
                    rate = (row[1] or 0) / row[0] * 100
                    last_week_rates.append(rate)
        
        last_week_avg = sum(last_week_rates) / len(last_week_rates) if last_week_rates else 0
        
        return {
            "this_week_rate": this_week_stats["avg_completion_rate"],
            "last_week_rate": round(last_week_avg, 1),
            "change": round(this_week_stats["avg_completion_rate"] - last_week_avg, 1)
        }

    def get_habit_forecast(self, username):
        habits = self.HabitManager.GetUserHabits(username)
        forecasts = []
        
        for habit in habits:
            habit_id = habit["id"]
            target_count = habit["target_count"]
            target_date_str = habit["target_date"]
            goal_type = habit["goal_type"]
            
            target_date = self._parse_date(target_date_str)
            if target_date is None:
                continue
            
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            
            with GetDBConnection(self.DBPath) as Conn:
                Cursor = Conn.cursor()
                Cursor.execute(
                    """SELECT AVG(count), AVG(suggested_target)
                    FROM habit_tracking
                    WHERE habit_id = ? AND date >= ? AND date <= ?""",
                    (habit_id, week_ago.isoformat(), today.isoformat())
                )
                row = Cursor.fetchone()
                if row and row[0] is not None:
                    avg_count = row[0]
                    avg_target = row[1] or target_count
                else:
                    continue
            
            if goal_type == "increase":
                progress_needed = target_count - avg_count
                daily_change = avg_count - (avg_count - (avg_target - avg_count))
                if daily_change > 0:
                    days_needed = progress_needed / daily_change
                    projected_date = today + datetime.timedelta(days=int(days_needed))
                else:
                    projected_date = target_date
            else:  # decrease
                progress_needed = avg_count - target_count
                daily_change = avg_count - avg_target
                if daily_change > 0:
                    days_needed = progress_needed / daily_change
                    projected_date = today + datetime.timedelta(days=int(days_needed))
                else:
                    projected_date = target_date
            
            forecasts.append({
                "habit_id": habit_id,
                "habit_name": habit["habit_name"],
                "target_date": target_date.isoformat(),
                "projected_date": projected_date.isoformat(),
                "on_track": projected_date <= target_date,
                "current_avg": round(avg_count, 1),
                "target": target_count
            })
        
        return forecasts

    def get_productivity_score(self, username, time_range="all_time"):
        task_stats = self.get_task_stats(username, time_range)
        habit_stats = self.get_habit_stats(username, time_range)

        task_score = task_stats["completion_rate"]
        habit_score = habit_stats["avg_completion_rate"]
        
        productivity_score = (task_score * 0.5) + (habit_score * 0.5) # 50/50 weighting
        
        return round(productivity_score, 1)

    def get_overall_trends(self, username, time_range="all_time"):
        task_trends = self.get_task_trends(username, time_range)
        habit_trends = self.get_habit_trends(username, time_range)
        
        all_dates = sorted(set[Any](task_trends["dates"] + habit_trends["dates"])) # concatenates dates, set removes ANY duplicates (however sets aren't ordered). sorted sorts the dates in ascending order.
        
        # Normalize to same date range
        combined_scores = []
        for date_str in all_dates:
            task_idx = task_trends["dates"].index(date_str) if date_str in task_trends["dates"] else -1 # .index() returns the first index of said value, but checks if date_str is in task_trends["dates"] first, if not returns -1 (so not found)
            task_score = task_trends["completion_rates"][task_idx] if task_idx >= 0 else 0 # if task_idx is not found, returns 0, otherwise returns the completion rate at the index of task_idx
            # SAME PROCESS FOR habits
            habit_idx = habit_trends["dates"].index(date_str) if date_str in habit_trends["dates"] else -1
            habit_score = habit_trends["completion_percentages"][habit_idx] if habit_idx >= 0 else 0
            
            # Combined score (50/50 weight)
            combined = (task_score * 0.5) + (habit_score * 0.5)
            combined_scores.append(combined)
        
        return {
            "dates": all_dates,
            "productivity_scores": combined_scores,
            "task_scores": [task_trends["completion_rates"][task_trends["dates"].index(d)] if d in task_trends["dates"] else 0 for d in all_dates], # if d (or could be any variable) is in task_trends["dates"], returns the completion rate at the index of d, otherwise returns 0
            "habit_scores": [habit_trends["completion_percentages"][habit_trends["dates"].index(d)] if d in habit_trends["dates"] else 0 for d in all_dates]

            # can freely use index d for both completion rates and dates as they are in the same order!
        }

