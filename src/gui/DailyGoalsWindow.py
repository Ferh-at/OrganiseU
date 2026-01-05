import customtkinter


class DailyGoalsWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username

        # Window configuration
        self.title("Daily Goals")
        self.geometry("600x700")
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
        }

        self.configure(fg_color=self.Colors["Light"])

        self._CreateUI()

    def _CreateUI(self):
        # Header
        HeaderFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=0
        )
        HeaderFrame.pack(fill="x", padx=0, pady=0)

        Title = customtkinter.CTkLabel(
            HeaderFrame,
            text="🎯 Daily Goals",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Date display
        DateFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Secondary"], corner_radius=10
        )
        DateFrame.pack(fill="x", padx=20, pady=20)

        from datetime import datetime

        TodayDate = datetime.now().strftime("%A, %B %d, %Y")

        DateLabel = customtkinter.CTkLabel(
            DateFrame,
            text=f"📅 {TodayDate}",
            text_color=self.Colors["Text"],
            font=("Montserrat", 14, "bold"),
        )
        DateLabel.pack(pady=15)

        # Goals list
        GoalsFrame = customtkinter.CTkScrollableFrame(
            self, fg_color="white", corner_radius=10
        )
        GoalsFrame.pack(fill="both", expand=True, padx=20, pady=10)

        # Sample goals
        SampleGoals = [
            "Complete 5 tasks from task manager",
            "Exercise for 30 minutes",
            "Work on personal project for 2 hours",
            "Read one chapter of a book",
            "Drink 8 glasses of water",
        ]

        for i, goal in enumerate(SampleGoals, 1):
            self._CreateGoalItem(GoalsFrame, i, goal)

        # Add goal button
        AddGoalBtn = customtkinter.CTkButton(
            self,
            text="➕ Add New Goal",
            fg_color=self.Colors["Secondary"],
            hover_color="#048A5E",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=45,
            command=self._AddGoal,
        )
        AddGoalBtn.pack(fill="x", padx=20, pady=10)

        # Close button
        CloseBtn = customtkinter.CTkButton(
            self,
            text="✕ Close",
            fg_color=self.Colors["Accent"],
            hover_color="#D97706",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13, "bold"),
            height=40,
            command=self.destroy,
        )
        CloseBtn.pack(pady=(0, 20))

    def _CreateGoalItem(self, parent, number, goal):
        GoalFrame = customtkinter.CTkFrame(
            parent, fg_color=self.Colors["Primary"], corner_radius=10
        )
        GoalFrame.pack(fill="x", padx=10, pady=8)

        GoalLabel = customtkinter.CTkLabel(
            GoalFrame,
            text=f"{number}. {goal}",
            text_color=self.Colors["Text"],
            font=("Montserrat", 13),
            anchor="w",
        )
        GoalLabel.pack(side="left", padx=15, pady=15, fill="x", expand=True)

        CheckBtn = customtkinter.CTkButton(
            GoalFrame,
            text="✓",
            fg_color=self.Colors["Secondary"],
            hover_color="#048A5E",
            text_color=self.Colors["Text"],
            width=40,
            height=30,
        )
        CheckBtn.pack(side="right", padx=10, pady=10)

    def _AddGoal(self):
        # Placeholder for add goal functionality
        print("Adding new goal...")
