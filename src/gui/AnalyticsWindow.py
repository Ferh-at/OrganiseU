import customtkinter
from core.TaskManager import TaskManager


class AnalyticsWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username
        self.TaskManager = TaskManager()

        # Window configuration
        self.title("Analytics Dashboard")
        self.geometry("900x700")
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
            text="📊 Analytics Dashboard",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Main content
        ContentFrame = customtkinter.CTkScrollableFrame(
            self, fg_color=self.Colors["Light"]
        )
        ContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # Stats overview
        Total, Completed, Pending = self.TaskManager.CountTasks(self.username)
        CompletionRate = int((Completed / Total * 100) if Total > 0 else 0)

        # Stat cards
        StatsFrame = customtkinter.CTkFrame(ContentFrame, fg_color=self.Colors["Light"])
        StatsFrame.pack(fill="x", pady=10)

        # Total tasks card
        self._CreateStatCard(
            StatsFrame, "📝 Total Tasks", str(Total), self.Colors["Primary"]
        ).pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Completed card
        self._CreateStatCard(
            StatsFrame, "✅ Completed", str(Completed), self.Colors["Secondary"]
        ).pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Pending card
        self._CreateStatCard(
            StatsFrame, "⏳ Pending", str(Pending), self.Colors["Accent"]
        ).pack(side="left", padx=10, pady=10, fill="both", expand=True)

        # Completion rate
        RateFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color=self.Colors["Dark"], corner_radius=15
        )
        RateFrame.pack(fill="x", padx=10, pady=20)

        RateTitle = customtkinter.CTkLabel(
            RateFrame,
            text="Completion Rate",
            text_color=self.Colors["Text"],
            font=("Montserrat", 18, "bold"),
        )
        RateTitle.pack(pady=(20, 10))

        RateValue = customtkinter.CTkLabel(
            RateFrame,
            text=f"{CompletionRate}%",
            text_color=self.Colors["Text"],
            font=("Montserrat", 48, "bold"),
        )
        RateValue.pack(pady=10)

        # Progress bar
        ProgressFrame = customtkinter.CTkFrame(
            RateFrame, fg_color=self.Colors["Light"], corner_radius=10, height=20
        )
        ProgressFrame.pack(fill="x", padx=50, pady=(10, 20))

        if Total > 0:
            ProgressBar = customtkinter.CTkFrame(
                ProgressFrame,
                fg_color=self.Colors["Secondary"],
                corner_radius=10,
                height=20,
            )
            ProgressBar.place(
                relx=0, rely=0, relwidth=CompletionRate / 100, relheight=1
            )

        # Insights section
        InsightsFrame = customtkinter.CTkFrame(
            ContentFrame, fg_color="white", corner_radius=15
        )
        InsightsFrame.pack(fill="x", padx=10, pady=10)

        InsightsTitle = customtkinter.CTkLabel(
            InsightsFrame,
            text="📈 Insights",
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 18, "bold"),
        )
        InsightsTitle.pack(pady=(20, 10))

        Insights = [
            f"🎯 You have {Pending} tasks to complete",
            f"✨ Great job completing {Completed} tasks!",
            "📅 Keep up the momentum!",
            "💪 Stay focused and organized",
        ]

        for insight in Insights:
            InsightLabel = customtkinter.CTkLabel(
                InsightsFrame,
                text=insight,
                text_color=self.Colors["TextDark"],
                font=("Montserrat", 13),
                anchor="w",
            )
            InsightLabel.pack(anchor="w", padx=30, pady=5)

        customtkinter.CTkLabel(InsightsFrame, text="").pack(pady=10)

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

    def _CreateStatCard(self, parent, title, value, color):
        Card = customtkinter.CTkFrame(parent, fg_color=color, corner_radius=12)

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
        ValueLabel.pack(pady=(5, 15))

        return Card
