import customtkinter
from datetime import datetime, timedelta


class CalendarWindow(customtkinter.CTkToplevel):
    def __init__(self, parent, username):
        super().__init__(parent)

        self.username = username

        # Window configuration
        self.title("Calendar")
        self.geometry("800x700")
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

        self.CurrentDate = datetime.now()

        self._CreateUI()

    def _CreateUI(self):
        # Header
        HeaderFrame = customtkinter.CTkFrame(
            self, fg_color=self.Colors["Primary"], corner_radius=0
        )
        HeaderFrame.pack(fill="x", padx=0, pady=0)

        Title = customtkinter.CTkLabel(
            HeaderFrame,
            text="📅 Calendar",
            text_color=self.Colors["Text"],
            font=("Montserrat", 24, "bold"),
        )
        Title.pack(pady=20)

        # Month navigation
        NavFrame = customtkinter.CTkFrame(self, fg_color=self.Colors["Light"])
        NavFrame.pack(fill="x", padx=20, pady=20)

        PrevBtn = customtkinter.CTkButton(
            NavFrame,
            text="◀",
            fg_color=self.Colors["Primary"],
            hover_color=self.Colors["Dark"],
            width=50,
            height=35,
            command=self._PreviousMonth,
        )
        PrevBtn.pack(side="left", padx=5)

        self.MonthLabel = customtkinter.CTkLabel(
            NavFrame,
            text=self.CurrentDate.strftime("%B %Y"),
            text_color=self.Colors["TextDark"],
            font=("Montserrat", 18, "bold"),
        )
        self.MonthLabel.pack(side="left", expand=True)

        NextBtn = customtkinter.CTkButton(
            NavFrame,
            text="▶",
            fg_color=self.Colors["Primary"],
            hover_color=self.Colors["Dark"],
            width=50,
            height=35,
            command=self._NextMonth,
        )
        NextBtn.pack(side="right", padx=5)

        # Calendar grid
        CalendarFrame = customtkinter.CTkFrame(self, fg_color="white", corner_radius=10)
        CalendarFrame.pack(fill="both", expand=True, padx=20, pady=10)

        # Day headers
        Days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(Days):
            DayHeader = customtkinter.CTkLabel(
                CalendarFrame,
                text=day,
                text_color=self.Colors["TextDark"],
                font=("Montserrat", 12, "bold"),
            )
            DayHeader.grid(row=0, column=col, padx=5, pady=10, sticky="nsew")

        # Calendar days (simplified)
        for row in range(1, 6):
            for col in range(7):
                day_num = (row - 1) * 7 + col + 1
                if day_num <= 31:
                    DayButton = customtkinter.CTkButton(
                        CalendarFrame,
                        text=str(day_num),
                        fg_color=self.Colors["Light"],
                        hover_color=self.Colors["Primary"],
                        text_color=self.Colors["TextDark"],
                        width=80,
                        height=60,
                    )
                    DayButton.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Configure grid weights
        for i in range(7):
            CalendarFrame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            CalendarFrame.grid_rowconfigure(i, weight=1)

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

    def _PreviousMonth(self):
        self.CurrentDate = self.CurrentDate - timedelta(days=30)
        self.MonthLabel.configure(text=self.CurrentDate.strftime("%B %Y"))

    def _NextMonth(self):
        self.CurrentDate = self.CurrentDate + timedelta(days=30)
        self.MonthLabel.configure(text=self.CurrentDate.strftime("%B %Y"))
