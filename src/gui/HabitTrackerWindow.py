import customtkinter


class HabitTrackerWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username

        # Window configuration
        self.title("Habit Tracker")
        self.geometry("900x650")
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
            text="🎯 Habit Tracker",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Main content frame
        ContentFrame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=10)
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        InfoLabel = customtkinter.CTkLabel(
            ContentFrame,
            text="Track your daily habits and build consistency! 💪",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 16, "bold"),
        )
        InfoLabel.pack(pady=30)

        # Sample habits display
        HabitsFrame = customtkinter.CTkScrollableFrame(
            ContentFrame, fg_color=self.Colors["Light"], corner_radius=10
        )
        HabitsFrame.pack(fill="both", expand=True, padx=20, pady=20)

        SampleHabits = [
            "💧 Drink 8 glasses of water",
            "🏃 Exercise for 30 minutes",
            "📖 Read for 20 minutes",
            "🧘 Meditate for 10 minutes",
            "💤 Sleep before 11 PM",
        ]

        for habit in SampleHabits:
            HabitCard = customtkinter.CTkFrame(
                HabitsFrame, fg_color=self.Colors["Primary"], corner_radius=8
            )
            HabitCard.pack(fill="x", padx=10, pady=8)

            HabitLabel = customtkinter.CTkLabel(
                HabitCard,
                text=habit,
                text_color=self.Colors["Text"],
                font=("Montserrat", 13),
                anchor="w",
            )
            HabitLabel.pack(side="left", padx=15, pady=12)

            CheckBtn = customtkinter.CTkButton(
                HabitCard,
                text="✓",
                fg_color=self.Colors["Secondary"],
                hover_color="#048A5E",
                text_color=self.Colors["Text"],
                width=50,
                height=30,
            )
            CheckBtn.pack(side="right", padx=10, pady=8)

        # Bottom buttons
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
