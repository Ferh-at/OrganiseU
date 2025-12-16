import customtkinter
import datetime
from core.HabitManager import HabitManager
from gui.AddHabitWindow import AddHabitWindow


class HabitTrackerWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username
        self.HabitManager = HabitManager()

        # Window configuration
        self.title("Habit Tracker")
        self.geometry("950x700")
        self.attributes("-topmost", True)

        # Color palette
        self.Colors = {
            "Primary": "#2E86AB",
            "Secondary": "#06A77D",
            "Accent": "#F18F01",
            "Dark": "#1B263B",
            "Light": "#E8F4F8",
            "Text": "#FFFFFF",
            "TextDark": "#1B263B",
            "Success": "#06A77D",
            "Warning": "#F18F01",
            "Danger": "#D32F2F",
        }

        self.configure(fg_color=self.Colors["Light"])

        self.HabitManager.CheckAndGenerateDailyGoals(self.username)

        self._CreateUI()
        self._LoadHabits()

    def _CreateUI(self):
        HeaderFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=0
        )
        HeaderFrame.pack(fill="x", padx=0, pady=0)

        Title = customtkinter.CTkLabel(
            HeaderFrame,
            text="🎯 Habit Tracker",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        AddButtonFrame = customtkinter.CTkFrame(self, fg_color=self.Colors["Light"])
        AddButtonFrame.pack(fill="x", padx=20, pady=(20, 10))

        AddHabitBtn = customtkinter.CTkButton(
            AddButtonFrame,
            text="➕ Add New Habit",
            fg_color=self.Colors["Secondary"],
            hover_color=self.Colors["Success"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self._AddHabit,
        )
        AddHabitBtn.pack(side="left", padx=5)

        RefreshBtn = customtkinter.CTkButton(
            AddButtonFrame,
            text="🔄 Refresh",
            fg_color=self.Colors["Primary"],
            hover_color=self.Colors["Dark"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self._LoadHabits,
        )
        RefreshBtn.pack(side="left", padx=5)

        self.HabitsFrame = customtkinter.CTkScrollableFrame(
            self, fg_color="white", corner_radius=10
        )
        self.HabitsFrame.pack(fill="both", expand=True, padx=20, pady=10)

        ButtonFrame = customtkinter.CTkFrame(self, fg_color=self.Colors["Light"])
        ButtonFrame.pack(fill="x", padx=20, pady=(0, 20))

        CloseBtn = customtkinter.CTkButton(
            ButtonFrame,
            text="✕ Close",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self.destroy,
        )
        CloseBtn.pack(side="right", padx=5)

    def _LoadHabits(self):
        """Load and display all user habits"""
        for widget in self.HabitsFrame.winfo_children():
            widget.destroy()

        habits = self.HabitManager.GetUserHabits(self.username)

        if not habits:
            NoHabitsLabel = customtkinter.CTkLabel(
                self.HabitsFrame,
                text="No habits yet. Click 'Add New Habit' to get started!",
                text_color=self.Colors["TextDark"],
                font=("Montserrat", 14),
            )
            NoHabitsLabel.pack(pady=50)
            return

        for habit in habits:
            self._CreateHabitCard(habit)

    def _CreateHabitCard(self, habit):
        habit_id = habit["id"]
        today_data = self.HabitManager.GetTodayData(habit_id)

        if not today_data:
            return

        count = today_data["count"]
        target = today_data["suggested_target"]
        goal_type = habit["goal_type"]

        target_date = datetime.datetime.strptime(
            habit["target_date"], "%Y-%m-%d"
        ).date()
        today = datetime.date.today()
        days_remaining = (target_date - today).days

        if goal_type == "increase":
            if count >= target:
                card_color = self.Colors["Success"]  
            elif count >= target * 0.7:
                card_color = self.Colors["Primary"]  
            else:
                card_color = self.Colors["Warning"]  
        else:  # decrease
            if count <= target:
                card_color = self.Colors["Success"]  
            elif count <= target * 1.3:
                card_color = self.Colors["Primary"]  
            else:
                card_color = self.Colors["Danger"]  

        HabitCard = customtkinter.CTkFrame(
            self.HabitsFrame, fg_color=card_color, corner_radius=10
        )
        HabitCard.pack(fill="x", padx=10, pady=10)

        LeftFrame = customtkinter.CTkFrame(HabitCard, fg_color="transparent")
        LeftFrame.pack(side="left", fill="both", expand=True, padx=15, pady=12)

        HabitNameLabel = customtkinter.CTkLabel(
            LeftFrame,
            text=habit["habit_name"],
            text_color=self.Colors["Text"],
            font=("Montserrat", 15, "bold"),
            anchor="w",
        )
        HabitNameLabel.pack(anchor="w")

        ProgressText = f"Today: {count} / {target}"
        if goal_type == "decrease":
            ProgressText += " (goal: decrease)"
        else:
            ProgressText += " (goal: increase)"

        ProgressLabel = customtkinter.CTkLabel(
            LeftFrame,
            text=ProgressText,
            text_color=self.Colors["Text"],
            font=("Montserrat", 12),
            anchor="w",
        )
        ProgressLabel.pack(anchor="w", pady=(3, 0))

        if days_remaining > 0:
            DaysText = f"📅 {days_remaining} days until deadline"
        elif days_remaining == 0:
            DaysText = "📅 Deadline is TODAY!"
        else:
            DaysText = "⚠️ Deadline passed"

        DaysLabel = customtkinter.CTkLabel(
            LeftFrame,
            text=DaysText,
            text_color=self.Colors["Text"],
            font=("Montserrat", 10),
            anchor="w",
        )
        DaysLabel.pack(anchor="w", pady=(3, 0))

        RightFrame = customtkinter.CTkFrame(HabitCard, fg_color="transparent")
        RightFrame.pack(side="right", padx=10, pady=10)

        IncrementBtn = customtkinter.CTkButton(
            RightFrame,
            text="+1",
            fg_color=self.Colors["Dark"],
            hover_color="#0D1B2A",
            text_color=self.Colors["Text"],
            font=("Montserrat", 16, "bold"),
            width=70,
            height=50,
            command=lambda: self._IncrementHabit(habit_id),
        )
        IncrementBtn.pack(side="left", padx=5)

        DeleteBtn = customtkinter.CTkButton(
            RightFrame,
            text="🗑️",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            width=50,
            height=50,
            command=lambda: self._DeleteHabit(habit_id),
        )
        DeleteBtn.pack(side="left", padx=5)

    def _AddHabit(self):
        """Open Add Habit window"""
        AddHabitWindow(self, self.username, self.HabitManager, self._LoadHabits)

    def _IncrementHabit(self, habit_id):
        """Increment habit count by 1"""
        self.HabitManager.IncrementHabit(habit_id)
        self._LoadHabits()

    def _DeleteHabit(self, habit_id):
        """Delete a habit with confirmation"""
        ConfirmDialog = customtkinter.CTkToplevel(self)
        ConfirmDialog.title("Confirm Delete")
        ConfirmDialog.geometry("400x180")
        ConfirmDialog.attributes("-topmost", True)
        ConfirmDialog.configure(fg_color=self.Colors["Light"])

        MsgLabel = customtkinter.CTkLabel(
            ConfirmDialog,
            text="Are you sure you want to delete this habit?\nAll tracking data will be lost.",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 12),
            justify="center",
        )
        MsgLabel.pack(pady=30)

        BtnFrame = customtkinter.CTkFrame(ConfirmDialog, fg_color=self.Colors["Light"])
        BtnFrame.pack(pady=10)

        def ConfirmDelete():
            self.HabitManager.DeleteHabit(habit_id)
            self._LoadHabits()
            ConfirmDialog.destroy()

        YesBtn = customtkinter.CTkButton(
            BtnFrame,
            text="Yes, Delete",
            fg_color=self.Colors["Danger"],
            hover_color="#B71C1C",
            text_color=self.Colors["Text"],
            width=120,
            command=ConfirmDelete,
        )
        YesBtn.pack(side="left", padx=10)

        NoBtn = customtkinter.CTkButton(
            BtnFrame,
            text="Cancel",
            fg_color=self.Colors["Dark"],
            hover_color=self.Colors["Primary"],
            text_color=self.Colors["Text"],
            width=120,
            command=ConfirmDialog.destroy,
        )
        NoBtn.pack(side="left", padx=10)
