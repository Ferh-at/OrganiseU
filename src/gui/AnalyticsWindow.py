import customtkinter
from PIL import Image
import os
import tempfile
from core.AnalyticsProcessor import AnalyticsProcessor
from utils.ChartGenerator import (
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_multi_line_chart,
    get_temp_chart_path,
)


class AnalyticsWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username
        self.processor = AnalyticsProcessor()
        self.current_time_range = "all_time"
        self.chart_paths = []  # Track chart files for cleanup

        self.title("Analytics Dashboard")
        self.geometry("1200x800")
        self.attributes("-topmost", True)

        self.Colors = {
            "Primary": "#2E86AB",
            "Secondary": "#06A77D",
            "Accent": "#F18F01",
            "Dark": "#1B263B",
            "Light": "#E8F4F8",
            "Text": "#FFFFFF",
            "TextDark": "#1B263B",
        }

        self.configure(fg_color=self.Colors["Light"])

        self._CreateUI()

        # Cleanup chart files on window close
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self):
        for path in self.chart_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
        self.destroy()

    def _CreateUI(self):
        HeaderFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=0
        )
        HeaderFrame.pack(fill="x", padx=0, pady=0)

        TitleFrame = customtkinter.CTkFrame(HeaderFrame, fg_color="transparent")
        TitleFrame.pack(side="left", padx=20, pady=15)

        Title = customtkinter.CTkLabel(
            TitleFrame,
            text="Analytics Dashboard",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(side="left")

        RangeFrame = customtkinter.CTkFrame(HeaderFrame, fg_color="transparent")
        RangeFrame.pack(side="right", padx=20, pady=15)

        self.TimeRangeSelector = customtkinter.CTkOptionMenu(
            RangeFrame,
            values=["Today", "This Week", "This Month", "All Time"],
            command=self._on_time_range_change,
            fg_color=self.Colors["Secondary"],
            button_color=self.Colors["Dark"],
            button_hover_color=self.Colors["Accent"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=150,
        )
        self.TimeRangeSelector.set("All Time")
        self.TimeRangeSelector.pack(side="right", padx=10)

        RefreshBtn = customtkinter.CTkButton(
            RangeFrame,
            text="Refresh",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 12, "bold"),
            width=100,
            height=35,
            command=self._refresh_analytics,
        )
        RefreshBtn.pack(side="right", padx=5)

        self.ContentFrame = customtkinter.CTkScrollableFrame(
            self, fg_color=self.Colors["Light"]
        )
        self.ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        self._update_dashboard()

    def _on_time_range_change(self, value):
        mapping = {
            "Today": "today",
            "This Week": "this_week",
            "This Month": "this_month",
            "All Time": "all_time",
        }
        self.current_time_range = mapping.get(value, "all_time")
        self._update_dashboard()

    def _refresh_analytics(self):
        self._update_dashboard()

    def _update_dashboard(self):
        for widget in self.ContentFrame.winfo_children():
            widget.destroy()

        # Clean up old chart files
        for path in self.chart_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except:
                pass
        self.chart_paths.clear()

        self._create_dashboard_cards()
        self._create_charts_section()
        self._create_insights_section()

        CloseBtn = customtkinter.CTkButton(
            self.ContentFrame,
            text="Close",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            width=150,
            command=self._on_closing,
        )
        CloseBtn.pack(pady=20)

    def _create_dashboard_cards(self):
        CardsFrame = customtkinter.CTkFrame(
            self.ContentFrame, fg_color=self.Colors["Light"]
        )
        CardsFrame.pack(fill="x", pady=10)
        CardsFrame.grid_columnconfigure(0, weight=1)
        CardsFrame.grid_columnconfigure(1, weight=1)
        CardsFrame.grid_columnconfigure(2, weight=1)
        CardsFrame.grid_columnconfigure(3, weight=1)

        task_stats = self.processor.get_task_stats(self.username, self.current_time_range)
        habit_stats = self.processor.get_habit_stats(self.username, self.current_time_range)
        productivity_score = self.processor.get_productivity_score(self.username, self.current_time_range)

        streaks = self.processor.get_habit_streaks(self.username)

        longest_streak = 0
        longest_streak_habit = "None"
        for _, streak_data in streaks.items():
            if streak_data["current_streak"] > longest_streak:
                longest_streak = streak_data["current_streak"]
                longest_streak_habit = streak_data["habit_name"]

        self._CreateDashboardCard(
            CardsFrame,
            "Task Completion",
            f"{task_stats['completion_rate']}%",
            f"{task_stats['completed']}/{task_stats['total']} tasks",
            self.Colors["Primary"],
            0,
            0,
            lambda: self._show_task_details(),)

        self._CreateDashboardCard(
            CardsFrame,
            "Active Habits",
            str(habit_stats["active_habits"]),
            f"{habit_stats['avg_completion_rate']}% avg completion",
            self.Colors["Secondary"],
            0,
            1,
            lambda: self._show_habit_details(),
        )

        self._CreateDashboardCard(
            CardsFrame,
            "Current Streak",
            f"{longest_streak} days",
            longest_streak_habit,
            self.Colors["Accent"],
            0,
            2,
            lambda: self._show_streak_details(),
        )

        self._CreateDashboardCard(
            CardsFrame,
            "Productivity Score",
            f"{productivity_score}%",
            "Combined tasks + habits",
            self.Colors["Dark"],
            0,
            3,
            lambda: self._show_productivity_details(),
        )

    def _CreateDashboardCard(
        self, parent, title, value, subtitle, color, row, col, command):
        Card = customtkinter.CTkFrame(
            parent, fg_color=color, corner_radius=12, cursor="hand2"
        )
        Card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        Card.bind("<Button-1>", lambda e: command())

        TitleLabel = customtkinter.CTkLabel(
            Card,
            text=title,
            text_color=self.Colors["Text"],
            font=("Montserrat", 14, "bold"),
        )
        TitleLabel.pack(pady=(15, 5))

        ValueLabel = customtkinter.CTkLabel(
            Card,
            text=value,
            text_color=self.Colors["Text"],
            font=("Montserrat", 36, "bold"),
        )
        ValueLabel.pack(pady=5)

        if "Completion" in title:
            task_stats = self.processor.get_task_stats(
                self.username, self.current_time_range
            )
            progress = task_stats["completion_rate"] / 100.0

            ProgressFrame = customtkinter.CTkFrame(
                Card, fg_color=self.Colors["Light"], corner_radius=5, height=8
            )
            ProgressFrame.pack(fill="x", padx=20, pady=(5, 10))

            if task_stats["total"] > 0:
                ProgressBar = customtkinter.CTkFrame(
                    ProgressFrame,
                    fg_color=self.Colors["Text"],
                    corner_radius=5,
                    height=8,
                )
                ProgressBar.place(relx=0, rely=0, relwidth=progress, relheight=1)

        SubtitleLabel = customtkinter.CTkLabel(
            Card,
            text=subtitle,
            text_color=self.Colors["Text"],
            font=("Montserrat", 11),
        )
        SubtitleLabel.pack(pady=(0, 15))

        # Make all child widgets clickable
        for widget in Card.winfo_children():
            widget.bind("<Button-1>", lambda e: command())

        return Card

    def _create_charts_section(self):
        self._create_task_completion_trends_chart()
        self._create_task_status_pie_chart()
        self._create_habit_performance_chart()
        self._create_habit_streaks_chart()
        self._create_week_comparison_chart()
        self._create_productivity_trend_chart()
        self._create_goal_forecast_chart()


    def _create_task_completion_trends_chart(self):
        trends = self.processor.get_task_trends(self.username, self.current_time_range)

        if not trends["dates"]:
            return

        chart_path = get_temp_chart_path("task_trends")
        self.chart_paths.append(chart_path)

        create_line_chart(
            trends["completion_rates"],
            "Task Completion Rate Trend",
            "Date",
            "Completion Rate (%)",
            chart_path,
            trends["dates"],
        )

        self._display_chart(chart_path, "Task Completion Trends")

    def _create_task_status_pie_chart(self):
        """Task Status Distribution - Pie Chart"""
        stats = self.processor.get_task_stats(self.username, self.current_time_range)

        if stats["total"] == 0:
            return

        data = {"Completed": stats["completed"], "Pending": stats["pending"]}

        chart_path = get_temp_chart_path("task_status")
        self.chart_paths.append(chart_path)

        create_pie_chart(data, "Task Status Distribution", chart_path)
        self._display_chart(chart_path, "Task Status Distribution")

    def _create_habit_performance_chart(self):
        habits = self.processor.HabitManager.GetUserHabits(self.username)

        if not habits:
            return

        start_date, end_date = self.processor._get_date_range(self.current_time_range)
        habit_data = {}

        for habit in habits:
            habit_id = habit["id"]
            if start_date is None:
                from utils.AuthenticationWrapper import GetDBConnection

                with GetDBConnection() as Conn:
                    Cursor = Conn.cursor()
                    Cursor.execute(
                        """SELECT COUNT(*), SUM(CASE WHEN count >= suggested_target THEN 1 ELSE 0 END)
                        FROM habit_tracking WHERE habit_id = ?""",
                        (habit_id,),
                    )
                    row = Cursor.fetchone()
                    if row and row[0] and row[0] > 0:
                        rate = (row[1] or 0) / row[0] * 100
                        habit_data[habit["habit_name"]] = rate
            else:
                start_str = start_date.isoformat()
                end_str = end_date.isoformat()
                from utils.AuthenticationWrapper import GetDBConnection

                with GetDBConnection() as Conn:
                    Cursor = Conn.cursor()
                    Cursor.execute(
                        """SELECT COUNT(*), SUM(CASE WHEN count >= suggested_target THEN 1 ELSE 0 END)
                        FROM habit_tracking 
                        WHERE habit_id = ? AND date >= ? AND date <= ?""",
                        (habit_id, start_str, end_str),
                    )
                    row = Cursor.fetchone()
                    if row and row[0] and row[0] > 0:
                        rate = (row[1] or 0) / row[0] * 100
                        habit_data[habit["habit_name"]] = rate

        if not habit_data:
            return

        chart_path = get_temp_chart_path("habit_performance")
        self.chart_paths.append(chart_path)

        create_bar_chart(
            habit_data,
            "Habit Completion Rates",
            "Habit",
            "Completion Rate (%)",
            chart_path,
        )
        self._display_chart(chart_path, "Habit Performance")

    def _create_habit_streaks_chart(self):
        streaks = self.processor.get_habit_streaks(self.username)

        if not streaks:
            return

        streak_data = {data["habit_name"]: data["current_streak"] for _, data in streaks.items()}

        if not streak_data:
            return

        chart_path = get_temp_chart_path("habit_streaks")
        self.chart_paths.append(chart_path)

        create_bar_chart(streak_data, "Current Habit Streaks", "Habit", "Days", chart_path)
        self._display_chart(chart_path, "Habit Streaks")

    def _create_week_comparison_chart(self):
        comparison = self.processor.get_task_comparison(self.username)

        data = {
            "Last Week": comparison["week_over_week"]["last_week"],
            "This Week": comparison["week_over_week"]["this_week"],
        }
        chart_path = get_temp_chart_path("week_comparison")
        self.chart_paths.append(chart_path)

        create_bar_chart(
            data,
            "Week-over-Week Task Completion",
            "Period",
            "Completion Rate (%)",
            chart_path,
        )
        self._display_chart(chart_path, "Week-over-Week Comparison")

    def _create_productivity_trend_chart(self):
        trends = self.processor.get_overall_trends(
            self.username, self.current_time_range
        )

        if not trends["dates"]:
            return

        data_dict = {
            "Productivity": trends["productivity_scores"],
            "Tasks": trends["task_scores"],
            "Habits": trends["habit_scores"],
        }

        chart_path = get_temp_chart_path("productivity_trend")
        self.chart_paths.append(chart_path)

        create_multi_line_chart(
            data_dict,
            "Productivity Trends",
            "Date",
            "Completion Rate (%)",
            chart_path,
            trends["dates"],
        )
        self._display_chart(chart_path, "Productivity Trends")

    def _create_goal_forecast_chart(self):
        """Goal Achievement Forecast - Line Chart"""
        forecasts = self.processor.get_habit_forecast(self.username)

        if not forecasts:
            return

        # Prepare data for chart
        habit_names = [f["habit_name"] for f in forecasts]
        on_track = [1 if f["on_track"] else 0 for f in forecasts]

        # Create a simple visualization
        forecast_data = {}
        for f in forecasts:
            days_ahead = "On Track" if f["on_track"] else "Behind"
            forecast_data[f["habit_name"]] = 1 if f["on_track"] else 0

        chart_path = get_temp_chart_path("goal_forecast")
        self.chart_paths.append(chart_path)

        create_bar_chart(
            forecast_data,
            "Habit Goal Achievement Status",
            "Habit",
            "Status (1=On Track, 0=Behind)",
            chart_path,
        )
        self._display_chart(chart_path, "Goal Achievement Forecast")

    def _display_chart(self, chart_path, title):
        """Display a chart image in the content frame"""
        ChartFrame = customtkinter.CTkFrame(
            self.ContentFrame, fg_color="white", corner_radius=15
        )
        ChartFrame.pack(fill="both", expand=False, padx=10, pady=10)

        TitleLabel = customtkinter.CTkLabel(
            ChartFrame,
            text=title,
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 16, "bold"),
        )
        TitleLabel.pack(pady=(15, 10))

        try:
            ChartImagePIL = Image.open(chart_path)
            ChartImage = customtkinter.CTkImage(
                light_image=ChartImagePIL,
                size=(ChartImagePIL.width, ChartImagePIL.height),
            )
            ChartLabel = customtkinter.CTkLabel(ChartFrame, image=ChartImage, text="")
            ChartLabel.pack(pady=(0, 15))
        except Exception as e:
            ErrorLabel = customtkinter.CTkLabel(
                ChartFrame,
                text=f"Error loading chart: {str(e)}",
                text_color="red",
                font=("Montserrat", 12),
            )
            ErrorLabel.pack(pady=15)

    def _create_insights_section(self):
        """Create dynamic insights section"""
        InsightsFrame = customtkinter.CTkFrame(
            self.ContentFrame, fg_color="white", corner_radius=15
        )
        InsightsFrame.pack(fill="x", padx=10, pady=10)

        InsightsTitle = customtkinter.CTkLabel(
            InsightsFrame,
            text="Insights",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 18, "bold"),
        )
        InsightsTitle.pack(pady=(20, 10))

        insights = self._generate_insights()

        for insight in insights:
            InsightLabel = customtkinter.CTkLabel(
                InsightsFrame,
                text=insight,
                text_color=self.Colors["TextDark"],
                font=("Montserrat", 13),
                anchor="w",
                justify="left",
            )
            InsightLabel.pack(anchor="w", padx=30, pady=5)

        customtkinter.CTkLabel(InsightsFrame, text="").pack(pady=10)

    def _generate_insights(self):
        """Generate dynamic insights based on data"""
        insights = []

        # Task insights
        task_stats = self.processor.get_task_stats(
            self.username, self.current_time_range
        )
        if task_stats["total"] > 0:
            insights.append(
                f"You've completed {task_stats['completed']} out of {task_stats['total']} tasks ({task_stats['completion_rate']}%)"
            )
            if task_stats["pending"] > 0:
                insights.append(
                    f"You have {task_stats['pending']} pending tasks to complete"
                )

        # Habit insights
        streaks = self.processor.get_habit_streaks(self.username)
        if streaks:
            longest_streak = 0
            longest_habit = ""
            for habit_id, data in streaks.items():
                if data["current_streak"] > longest_streak:
                    longest_streak = data["current_streak"]
                    longest_habit = data["habit_name"]
            if longest_streak > 0:
                insights.append(
                    f"Longest streak: {longest_habit} at {longest_streak} days"
                )

        # Forecast insights
        forecasts = self.processor.get_habit_forecast(self.username)
        if forecasts:
            on_track = [f for f in forecasts if f["on_track"]]
            if on_track:
                habit_name = on_track[0]["habit_name"]
                projected_date = on_track[0]["projected_date"]
                insights.append(
                    f"You're on track to complete '{habit_name}' by {projected_date}"
                )

        # Comparison insights
        comparison = self.processor.get_task_comparison(self.username)
        change = comparison["week_over_week"]["change"]
        if change > 0:
            insights.append(f"Your completion rate improved by {change}% this week!")
        elif change < 0:
            insights.append(
                f"Your completion rate decreased by {abs(change)}% this week"
            )

        # Productivity score
        productivity = self.processor.get_productivity_score(
            self.username, self.current_time_range
        )
        insights.append(f"Your productivity score is {productivity}%")

        if not insights:
            insights.append("Start tracking tasks and habits to see insights!")

        return insights

    # Drill-down methods
    def _show_task_details(self):
        """Show detailed task breakdown"""
        self._show_drill_down("Tasks", self._get_task_details_content())

    def _show_habit_details(self):
        """Show detailed habit breakdown"""
        self._show_drill_down("Habits", self._get_habit_details_content())

    def _show_streak_details(self):
        """Show detailed streak information"""
        self._show_drill_down("Streaks", self._get_streak_details_content())

    def _show_productivity_details(self):
        """Show productivity breakdown"""
        self._show_drill_down("Productivity", self._get_productivity_details_content())

    def _show_drill_down(self, title, content):
        """Display drill-down window with details"""
        DetailWindow = customtkinter.CTkToplevel(self)
        DetailWindow.title(f"{title} Details")
        DetailWindow.geometry("600x500")
        DetailWindow.attributes("-topmost", True)

        HeaderFrame = customtkinter.CTkFrame(
            DetailWindow, fg_color=self.Colors["Primary"], corner_radius=0
        )
        HeaderFrame.pack(fill="x")

        TitleLabel = customtkinter.CTkLabel(
            HeaderFrame,
            text=f"{title} Details",
            text_color=self.Colors["Text"],
            font=("Montserrat", 20, "bold"),
        )
        TitleLabel.pack(pady=15)

        ContentFrame = customtkinter.CTkScrollableFrame(
            DetailWindow, fg_color=self.Colors["Light"]
        )
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        for item in content:
            ItemLabel = customtkinter.CTkLabel(
                ContentFrame,
                text=item,
                text_color=self.Colors["TextDark"],
                font=("Montserrat", 12),
                anchor="w",
                justify="left",
            )
            ItemLabel.pack(anchor="w", padx=10, pady=5)

        CloseBtn = customtkinter.CTkButton(
            DetailWindow,
            text="Close",
            fg_color=self.Colors["Accent"],
            command=DetailWindow.destroy,
        )
        CloseBtn.pack(pady=10)

    def _get_task_details_content(self):
        """Get task details for drill-down"""
        content = []
        tasks = self.processor.TaskManager.GetTasks(self.username)

        stats = self.processor.get_task_stats(self.username, self.current_time_range)
        content.append(f"Total Tasks: {stats['total']}")
        content.append(f"Completed: {stats['completed']}")
        content.append(f"Pending: {stats['pending']}")
        content.append(f"Completion Rate: {stats['completion_rate']}%")
        content.append("")
        content.append("Task List:")

        for task_id, title, status, description in tasks:
            content.append(f"{title} ({status})")
            if description:
                content.append(f"   {description}")

        return content

    def _get_habit_details_content(self):
        """Get habit details for drill-down"""
        content = []
        habits = self.processor.HabitManager.GetUserHabits(self.username)

        stats = self.processor.get_habit_stats(self.username, self.current_time_range)
        content.append(f"Active Habits: {stats['active_habits']}")
        content.append(f"Average Completion Rate: {stats['avg_completion_rate']}%")
        content.append("")
        content.append("Habit Details:")

        for habit in habits:
            content.append(f"{habit['habit_name']}")
            content.append(f"   Goal: {habit['goal_type']} to {habit['target_count']}")
            content.append(f"   Target Date: {habit['target_date']}")

        return content

    def _get_streak_details_content(self):
        """Get streak details for drill-down"""
        content = []
        streaks = self.processor.get_habit_streaks(self.username)

        content.append("Current Streaks:")
        for habit_id, data in streaks.items():
            content.append(f"{data['habit_name']}: {data['current_streak']} days")
            content.append(f"   Longest streak: {data['longest_streak']} days")

        return content

    def _get_productivity_details_content(self):
        """Get productivity details for drill-down"""
        content = []

        task_stats = self.processor.get_task_stats(
            self.username, self.current_time_range
        )
        habit_stats = self.processor.get_habit_stats(
            self.username, self.current_time_range
        )
        productivity = self.processor.get_productivity_score(
            self.username, self.current_time_range
        )

        content.append(f"Overall Productivity Score: {productivity}%")
        content.append("")
        content.append("Breakdown:")
        content.append(
            f"  Task Completion: {task_stats['completion_rate']}% (50% weight)"
        )
        content.append(
            f"  Habit Completion: {habit_stats['avg_completion_rate']}% (50% weight)"
        )
        content.append("")
        content.append("Calculation:")
        content.append(
            f"  ({task_stats['completion_rate']} × 0.5) + ({habit_stats['avg_completion_rate']} × 0.5) = {productivity}%"
        )

        return content
